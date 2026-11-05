"""Optional MQTT (Tuya Smart Life / tuya_sharing) push support.

Bu modül tamamen OPSİYONEL bir katman — mevcut cloud/local polling
mimarisine hiç dokunmuyor, sadece üstüne "varsa kullan" şeklinde ekleniyor.

Nasıl çalışır (özet):
  1. Kurulum sırasında kullanıcı isterse (User Code + QR onayı) bir
     "tuya_sharing" (Smart Life uygulaması) girişi yapar. Bu, bizim
     asıl Access ID/Access Key ile kurduğumuz Cloud Development
     projesinden TAMAMEN AYRI, uyumsuz bir kimlik doğrulama sistemi
     (doğrulandı: /v2.0/cloud/thing/... uç noktalarına bu token ile
     erişilemiyor, "app param is invalid" hatası alınıyor) — bu yüzden
     sadece MQTT push almak için kullanılıyor, asıl veri çekme
     mekanizmamızı DEĞİŞTİRMİYOR.
  2. Bağlantı kurulunca, cihazın Tuya'nın "Standard Instruction Set"i
     üzerinden gördüğü DP'ler (device.function/status_range) bizim
     model dosyamızın ihtiyaç duyduğu DP kümesiyle karşılaştırılır:
       - Hepsi mevcutsa -> bu cihaz için periyodik poll DURAKLATILIR.
       - Bir tanesi bile eksikse -> periyodik poll AYNEN DEVAM EDER.
     Bu "yeterli/yetersiz" ayrımı SADECE poll'u duraklat/devam
     kararında kullanılır — gelen push'un İÇERİĞİ her durumda,
     koşulsuz olarak uygulanır (bkz. "ham mesaj" notu aşağıda);
     yetersizse AYRICA "bir şey değişti, tam sorgu da at" tetikleyicisi
     olarak kullanılır.
  3. MQTT bağlantısı koparsa, periyodik poll otomatik olarak eski
     haline döner — hiçbir zaman veri akışı tamamen kesilmez.

ÖNEMLİ — ham mesaj dinleyicisi (issue #111): `manager.add_device_
listener()` (SDK'nın kendi yüksek seviye API'si) KULLANILMIYOR, çünkü
SDK'nın kendi `_on_device_report()`'u, cihaz `support_local=True` ise
gelen DP'yi `device.local_strategy`'de YOKSA sessizce atlıyor — bazı
cihazlarda (örn. #111'de bildirilen e1k5wjuc modeli) bu, Tuya'nın
"Standard Instruction Set"i dışındaki (üreticiye özel) DP'lerin HİÇBİRİNİN
görülmemesine, dolayısıyla `update_device()`'in HİÇ tetiklenmemesine
(push'un tamamen etkisiz kalmasına, sadece periyodik poll'un çalışmasına)
yol açıyordu. Bunun yerine `manager.mq.add_message_listener()` ile
İKİNCİ, ham bir dinleyici ekleniyor — bu, SDK'nın kendi filtrelemesini
BYPASS ediyor, ham `{dpId veya code, value}` çiftlerini doğrudan görüyoruz.
dpId -> code çözümü `coordinator.dp_mapping` (model dosyasının kendi
tanımladığı, local moddaki _process_local_dps() ile AYNI eşleme)
üzerinden yapılıyor. `support_local=False` cihazlarda zaten SDK sunucu
tarafında çözülmüş `code` ile geliyor (filtre hiç devreye girmiyor); bu
yüzden dinleyicimiz HER İKİ şekli de (`dpId` VE doğrudan `code`) işliyor.

refresh_mq() her çağrıldığında `manager.mq` nesnesini BAŞTAN kuruyor (eski
mq.stop() edilip atılıyor) — yani her reconnect'te ham dinleyiciyi de
YENİDEN kaydetmek gerekiyor, yoksa sessizce düşer. _register_raw_listener()
bu yüzden her refresh_mq() çağrısından sonra ayrıca çağrılıyor.

Bu dosyadaki hiçbir şey, CONF_USER_CODE config_entry.data'da
tanımlanmadığı sürece devreye girmez — yani mevcut kurulumların
hiçbiri bundan etkilenmez.
"""
from __future__ import annotations

import asyncio
import logging
import time
from typing import Any

from homeassistant.core import HomeAssistant

from .const import DOMAIN, TUYA_SHARING_CLIENT_ID, TUYA_SHARING_SCHEMA

_LOGGER = logging.getLogger(__name__)

PROTOCOL_DEVICE_REPORT = 4


def _unwrap_login_result(result: Any) -> tuple[bool, dict | None]:
    """login_result() tuple ya da dict dönebiliyor (kütüphane sürümüne
    göre değişiyor) — ikisini de destekle. Test script'inde canlı
    doğrulanmış mantık, aynen taşındı."""
    if isinstance(result, tuple):
        first, second = result[0], result[1]
        if isinstance(first, bool):
            return first, second
        if isinstance(second, bool):
            return second, first
        return True, first
    if isinstance(result, dict):
        return bool(result.get("success")), result.get("result", result)
    return False, None


class SharingQRLogin:
    """Kurulum sırasında (config_flow.py) QR/User Code girişini yöneten
    yardımcı. Bir config flow oturumu boyunca TEK bir instance olarak
    tutulmalı (LoginControl'ün kendi iç durumu var — qr_code() ve
    login_result() çağrıları aynı token üzerinden birbirine bağlı)."""

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass
        self._login_control = None
        self._qr_token: str | None = None

    async def async_request_qr(self, user_code: str) -> dict:
        """QR kodu iste. Dönen dict'te "success" ve (başarılıysa)
        "result"->"qrcode" (token) bulunur."""
        from tuya_sharing import LoginControl

        def _do():
            if self._login_control is None:
                self._login_control = LoginControl()
            return self._login_control.qr_code(
                client_id=TUYA_SHARING_CLIENT_ID,
                schema=TUYA_SHARING_SCHEMA,
                user_code=user_code,
            )

        resp = await self._hass.async_add_executor_job(_do)
        if resp.get("success"):
            self._qr_token = resp["result"]["qrcode"]
        return resp

    async def async_check_login(self, user_code: str) -> tuple[bool, dict | None]:
        """Kullanıcı QR'ı onayladı mı diye bir kere kontrol eder (polling
        değil — config flow'un kendisi kullanıcının "Confirm" butonuna
        basmasını bekliyor, her basışta bu bir kere çağrılıyor)."""
        if self._qr_token is None or self._login_control is None:
            return False, None

        def _do():
            raw = self._login_control.login_result(
                token=self._qr_token,
                client_id=TUYA_SHARING_CLIENT_ID,
                user_code=user_code,
            )
            return _unwrap_login_result(raw)

        return await self._hass.async_add_executor_job(_do)

    @property
    def qr_token(self) -> str | None:
        """selector.QrCodeSelector için ham QR içeriği — HA'nın kendi
        yerleşik QR selector'ı bunu tarayıcıda anlık üretiyor, bizim
        PNG/dosya/data-URI ile uğraşmamıza hiç gerek yok (bkz. gerçek
        çalışan referans: azerty9971/xtend_tuya config_flow.py)."""
        if self._qr_token is None:
            return None
        return f"tuyaSmart--qrLogin?token={self._qr_token}"


def _collect_required_codes(model_mapping: dict) -> set[str]:
    """Model dosyasının GERÇEKTEN ihtiyaç duyduğu Tuya DP kodlarının
    tam kümesini çıkarır (raw field'larda raw_source, düzlerde code/key).
    dp_id'si olmayan (hesaplanmış/sanal) entry'ler hariç tutulur."""
    codes: set[str] = set()
    for entity_type in ("sensors", "binary_sensors", "switches", "numbers", "selects", "texts"):
        for key, cfg in model_mapping.get(entity_type, {}).items():
            if "dp_id" not in cfg:
                continue
            raw_source = cfg.get("raw_source")
            if raw_source:
                codes.add(raw_source)
            else:
                codes.add(cfg.get("code", key))
    return codes


def _device_covers_codes(device: Any, required_codes: set[str]) -> bool:
    """tuya_sharing'in bir cihaz için gördüğü DP kümesi (Standard
    Instruction Set'e kayıtlı olanlar), bizim ihtiyaç duyduğumuz TÜM
    kodları kapsıyor mu? Tek bir eksik bile varsa False — o cihaz için
    MQTT'ye güvenip periyodik poll'u kapatamayız."""
    available: set[str] = set()
    function = getattr(device, "function", None) or {}
    status_range = getattr(device, "status_range", None) or {}
    available.update(function.keys())
    available.update(status_range.keys())
    return required_codes.issubset(available)


class SharingMQTT:
    """Kurulum tamamlandıktan sonra (coordinator içinde) MQTT dinlemesini
    yöneten asıl sınıf. Token zaten config_entry.data'da mevcut olmalı
    (CONF_SHARING_TOKEN_INFO) — bu sınıf QR akışıyla ilgilenmez, sadece
    zaten onaylanmış bir girişi kullanır."""

    def __init__(self, hass: HomeAssistant, coordinator) -> None:
        self._hass = hass
        self._coordinator = coordinator
        self._manager = None
        self._sufficient = False
        self._connected = False
        self._reconnect_attempted = False
        self._health_check_task: asyncio.Task | None = None
        self._started_at = 0.0
        self._last_connect_refresh = 0.0

    @property
    def connected(self) -> bool:
        return self._connected

    @property
    def sufficient(self) -> bool:
        """Bu cihaz için MQTT'nin gördüğü DP kümesi, model dosyasının
        ihtiyaç duyduğu TÜM DP'leri kapsıyor mu? False ise periyodik
        poll ASLA duraklatılmamalı — push sadece tetikleyici olarak
        kullanılır, poll bağımsız çalışmaya devam etmeli."""
        return self._sufficient

    async def async_start(self) -> bool:
        """Bağlantıyı kurmayı dener. Başarısız olursa False döner —
        coordinator bunu "MQTT yok, periyodik poll'a devam" olarak
        yorumlamalı. Sonsuz backoff YOK, tek deneme (local moddaki
        _listen_loop ile aynı felsefe)."""
        from tuya_sharing import Manager

        from .const import CONF_SHARING_TOKEN_INFO, CONF_USER_CODE

        token_info = self._coordinator.config_entry.data.get(CONF_SHARING_TOKEN_INFO)
        user_code = self._coordinator.config_entry.data.get(CONF_USER_CODE)
        if not token_info or not user_code:
            return False

        if "terminal_id" not in token_info or "endpoint" not in token_info:
            from homeassistant.helpers import issue_registry as ir
            from .repairs import ISSUE_ID_TOKEN_INVALID

            _LOGGER.warning(
                "MQTT: kayıtlı token bilgisi eksik/bozuk (terminal_id ya "
                "da endpoint yok). Ayarlar → Sistem → Onarımlar sayfasında "
                "bunu düzeltmek için bir bildirim oluşturuldu."
            )
            ir.async_create_issue(
                self._hass,
                DOMAIN,
                ISSUE_ID_TOKEN_INVALID,
                is_fixable=True,
                is_persistent=True,
                severity=ir.IssueSeverity.WARNING,
                translation_key="mqtt_token_invalid",
                data={"entry_id": self._coordinator.config_entry.entry_id},
            )
            return False

        # Buraya kadar geldiysek token gecerli - eger daha once bir
        # onarim bildirimi acilmissa artik gecersiz, temizleyelim.
        from homeassistant.helpers import issue_registry as ir
        from .repairs import ISSUE_ID_TOKEN_INVALID
        ir.async_delete_issue(self._hass, DOMAIN, ISSUE_ID_TOKEN_INVALID)

        try:
            token_listener = _PersistTokenListener(self._hass, self._coordinator)

            def _build_manager():
                return Manager(
                    TUYA_SHARING_CLIENT_ID,
                    user_code,
                    token_info["terminal_id"],
                    token_info["endpoint"],
                    token_info,
                    token_listener,
                )

            self._manager = await self._hass.async_add_executor_job(_build_manager)

            await self._hass.async_add_executor_job(self._manager.update_device_cache)

            device = self._manager.device_map.get(self._coordinator.device_id)
            if device is None:
                _LOGGER.warning(
                    "MQTT: cihaz (%s) tuya_sharing hesabında bulunamadı — "
                    "muhtemelen bu hesapla paylaşılmamış. Periyodik poll ile devam.",
                    self._coordinator.device_id,
                )
                return False

            # refresh_mq() sadece set_up=True olan cihazları MQTT'ye
            # kaydediyor — bazı hesap/cihaz kombinasyonlarında bu bayrak
            # hiç True gelmiyor (canlı testte doğrulandı), o yüzden
            # gerekirse elle zorluyoruz.
            if not getattr(device, "set_up", False):
                try:
                    device.set_up = True
                except Exception:
                    pass

            await self._hass.async_add_executor_job(self._manager.refresh_mq)
            self._register_raw_listener()
            await asyncio.sleep(3)

            # Yeterlilik kontrolünü BURAYA (refresh_mq + bekleme sonrasına)
            # taşıdık — canlı testte gördük ki update_device_cache()'in
            # hemen ardından device.function/status_range bazen henüz
            # tam dolmuyor (örn. bir cihazda function'da temp_current
            # eksikken birkaç saniye sonra status_range'de doğru şekilde
            # görünüyordu). Cihaz nesnesini de device_map'ten TAZE
            # tekrar çekiyoruz, ihtimal dahilinde daha guncel bir
            # snapshot icin.
            device = self._manager.device_map.get(self._coordinator.device_id) or device
            # Ham dinleyici dpId'yi model dp_mapping ile kodladığı için
            # standart talimat setine (device.function/status_range)
            # bakmaya gerek yok: model dp_mapping doluysa push yeterli
            # sayılır ve sık poll yerine seyrek güvenlik poll'u kullanılır.
            self._sufficient = bool(getattr(self._coordinator, "dp_mapping", None))
            _LOGGER.info(
                "MQTT: cihaz %s için DP kapsama durumu: %s",
                self._coordinator.device_id,
                "yeterli (sık poll kapatılacak, seyrek güvenlik poll'u)" if self._sufficient else "yetersiz (dp_mapping boş, poll devam edecek)",
            )

            mq = getattr(self._manager, "mq", None)
            client = getattr(mq, "client", None) if mq else None
            if client is None:
                _LOGGER.warning("MQTT bağlantısı kurulamadı. Periyodik poll ile devam.")
                return False

            self._connected = True
            self._started_at = time.monotonic()
            self._health_check_task = self._hass.loop.create_task(self._health_check_loop())
            return True

        except Exception as err:
            _LOGGER.warning("MQTT başlatılamadı (%s). Periyodik poll ile devam.", err)
            return False

    @staticmethod
    def _client_is_connected(mq) -> bool:
        client = getattr(mq, "client", None) if mq else None
        return bool(client and getattr(client, "is_connected", lambda: False)())

    async def _health_check_loop(self) -> None:
        """Hafif bir bağlantı kontrolü (yalnızca yerel bir bayrak okur,
        ağ trafiği yaratmaz) — 60 sn'de bir.

        - Bağlantı koptuysa: sık poll'u hemen geri açar (coordinator).
        - Yeniden bağlanmayı GERİ ÇEKİLMELİ aralıklarla (1, 2, 5, sonra
          her 10 dk) SÜRESİZ dener — eskiden tek deneme yapıp pes
          ediyordu ve HA restart'a kadar MQTT bir daha hiç dönmüyordu.
        - Bağlantı (SDK'nın kendi otomatik yeniden bağlanmasıyla)
          kendiliğinden geri gelirse bunu fark edip güvenlik poll'una
          döner ve kopukluk sırasında kaçan değişiklikler için bir
          kerelik refresh yapar.
        """
        backoff = (60, 120, 300, 600)
        failures = 0
        next_retry_at = 0.0
        loop = asyncio.get_running_loop()
        while True:
            await asyncio.sleep(60)
            mq = getattr(self._manager, "mq", None)
            is_connected = self._client_is_connected(mq)

            if is_connected:
                failures = 0
                if not self._connected:
                    self._connected = True
                    _LOGGER.info("MQTT: bağlantı geri geldi.")
                    if self._sufficient:
                        self._coordinator._mqtt_set_active(True)
                    # Kopukluk sırasında kaçan değişiklikler için bir kez tazele.
                    self._hass.async_create_task(self._coordinator.async_request_refresh())
                continue

            if self._connected:
                _LOGGER.warning("MQTT bağlantısı koptu tespit edildi.")
                self._connected = False
                if self._sufficient:
                    self._coordinator._mqtt_set_active(False)
                next_retry_at = 0.0

            now = loop.time()
            if now < next_retry_at:
                continue

            _LOGGER.info("MQTT: yeniden bağlanma deneniyor (deneme %d)...", failures + 1)
            try:
                await self._hass.async_add_executor_job(self._manager.refresh_mq)
                self._register_raw_listener()
                await asyncio.sleep(5)
                if self._client_is_connected(getattr(self._manager, "mq", None)):
                    failures = 0
                    self._connected = True
                    if self._sufficient:
                        self._coordinator._mqtt_set_active(True)
                    self._hass.async_create_task(self._coordinator.async_request_refresh())
                    _LOGGER.info("MQTT: yeniden bağlanma başarılı.")
                    continue
            except Exception as err:
                _LOGGER.warning("MQTT: yeniden bağlanma denemesi başarısız (%s).", err)
            failures += 1
            next_retry_at = loop.time() + backoff[min(failures - 1, len(backoff) - 1)]

    async def async_stop(self) -> None:
        if self._health_check_task:
            self._health_check_task.cancel()
        self._coordinator._mqtt_cancel_safety_poll()
        mq = getattr(self._manager, "mq", None) if self._manager else None
        stop = getattr(mq, "stop", None) if mq else None
        if callable(stop):
            try:
                await self._hass.async_add_executor_job(stop)
            except Exception:
                pass

    def _register_raw_listener(self) -> None:
        """manager.mq.add_message_listener() ile ham dinleyiciyi kaydeder.
        refresh_mq() HER çağrıldığında manager.mq'yu baştan kurduğu için
        (eski mq.stop() edilip atılıyor), bu her refresh_mq() çağrısından
        SONRA tekrar çağrılmalı — yoksa reconnect sonrası dinleyici
        sessizce düşer."""
        mq = getattr(self._manager, "mq", None)
        if mq is not None:
            mq.add_message_listener(self._on_raw_message)
            self._hook_on_connect(mq)

    def _hook_on_connect(self, mq) -> None:
        """paho istemcisinin on_connect geri çağrısına (zincirleyerek) bağlanır:
        SDK bağlantıyı KENDİ KENDİNE (60 sn'lik sağlık kontrolümüzün göremeyeceği
        kadar kısa sürede) yeniden kurarsa, aradaki değişiklikler kaçmış
        olabilir; her yeniden bağlanmada bir kerelik tazeleme yaparız.
        Başarısız olursa sessizce atlanır, sağlık kontrolü yine çalışır."""
        client = getattr(mq, "client", None)
        if client is None or getattr(client, "_th_on_connect_hooked", False):
            return
        try:
            original = getattr(client, "on_connect", None)
            loop = self._hass.loop

            def _wrapped(*args, **kwargs):
                try:
                    if callable(original):
                        return original(*args, **kwargs)
                finally:
                    loop.call_soon_threadsafe(self._on_stream_connected)

            client.on_connect = _wrapped
            client._th_on_connect_hooked = True
        except Exception as err:  # noqa: BLE001
            _LOGGER.debug("MQTT on_connect kancası kurulamadı: %s", err)

    def _on_stream_connected(self) -> None:
        now = time.monotonic()
        # Başlangıç sorgusu zaten yeni yapıldı; çok sık tekrarı da engelle.
        if now - self._started_at < 30 or now - self._last_connect_refresh < 60:
            return
        self._last_connect_refresh = now
        _LOGGER.info("MQTT: akış yeniden bağlandı — kaçan değişiklikler için bir kez tazeleniyor.")
        self._hass.async_create_task(self._coordinator.async_request_refresh())

    def _on_raw_message(self, msg: dict) -> None:
        """manager.mq'ya ham dinleyici olarak eklenen fonksiyon (bkz.
        modül docstring'indeki "ham mesaj dinleyicisi" notu, issue #111)
        — tuya_sharing'in arka plan MQTT thread'inden çağrılıyor, HA
        event loop'una güvenli geçiş şart (call_soon_threadsafe /
        run_coroutine_threadsafe kullanmadan coordinator'a dokunmak
        thread-safety ihlali olur).

        SDK'nın kendi filtrelemesini (local_strategy dpId kontrolü)
        BYPASS ediyoruz — bu yüzden gelen item iki şekilden birinde
        olabilir (bkz. tuya_sharing/manager.py _on_device_report):
          - support_local=True cihaz: {"dpId": int, "value": ...} —
            dpId'yi coordinator.dp_mapping üzerinden code'a çözüyoruz
            (model dosyasının kendi eşlemesi, local moddakiyle AYNI
            kaynak — bulut thing model'ine hiç ihtiyaç yok).
          - support_local=False cihaz: {"code": str, "value": ...} —
            zaten sunucu tarafında çözülmüş, dpId hiç yok.
        İçerik HER ZAMAN koşulsuz uygulanır — "yeterli/yetersiz" ayrımı
        sadece periyodik poll'u duraklat/devam kararında kullanılıyor,
        push'un içeriğine güvenip güvenmeme kararında DEĞİL."""
        try:
            if msg.get("protocol") != PROTOCOL_DEVICE_REPORT:
                return
            data = msg.get("data", {}) or {}
            if data.get("devId") != self._coordinator.device_id:
                return

            # Bu cihazdan GELEN HER mesaj (tanınmayan DP'ler dahil) "cihaz
            # yaşıyor" kanıtıdır: son görülme zamanını güncelle.
            status_items = data.get("status", []) or []
            stamps = [
                it.get("t") for it in status_items
                if isinstance(it, dict) and isinstance(it.get("t"), (int, float))
            ]
            self._hass.loop.call_soon_threadsafe(
                self._coordinator._mqtt_note_message,
                max(stamps) if stamps else None,
                len(status_items) or 1,
            )


            dp_mapping = getattr(self._coordinator, "dp_mapping", None) or {}
            new_data: dict[str, Any] = {}
            for item in data.get("status", []) or []:
                if "value" not in item:
                    continue
                code = item.get("code")
                if code is None:
                    dp_id = item.get("dpId")
                    if dp_id is None:
                        continue
                    code = dp_mapping.get(dp_id)
                    if code is None:
                        continue
                new_data[code] = {"value": item["value"]}

            if new_data:
                self._hass.loop.call_soon_threadsafe(
                    self._coordinator._mqtt_apply_push, new_data
                )
            if not self._sufficient:
                # Yetersiz kapsamada push, İÇERİĞİNE bakılmaksızın ayrıca
                # "bir şey değişti, tam bir sorgu tetikle" sinyali olarak
                # da kullanılıyor — new_data boş olsa (örn. tamamen
                # tanınmayan bir DP) bile.
                asyncio.run_coroutine_threadsafe(
                    self._coordinator._mqtt_trigger_refresh(), self._hass.loop
                )
        except Exception as err:
            _LOGGER.debug("MQTT ham mesaj işlenirken hata: %s", err)


class _PersistTokenListener:
    """Token yenilenince (tuya_sharing kendi içinde otomatik yapıyor)
    config_entry.data'ya kalıcı olarak yazar — yoksa HA her restart'ta
    kullanıcı tekrar QR okutmak zorunda kalır."""

    def __new__(cls, hass: HomeAssistant, coordinator):
        from tuya_sharing import SharingTokenListener
        from .const import CONF_SHARING_TOKEN_INFO

        # config_entry NESNESİNİ değil, sadece sabit entry_id'sini
        # yakalıyoruz. Eğer entegrasyon reload olursa (örn. onarım
        # akışı sonunda), ESKİ SharingMQTT örneğinin arka plan thread'i
        # tam durmadan bir token yenileme daha tetiklerse, bayat bir
        # config_entry nesne referansını kullanıp güncel veriyi
        # kaçırma riski oluyordu — canlı ortamda "terminal_id kayboldu"
        # olarak gözlemlendi. Her yazmada HA'dan TAZE entry çekerek bu
        # riski tamamen ortadan kaldırıyoruz.
        entry_id = coordinator.config_entry.entry_id

        def _persist(token_info: dict) -> None:
            entry = hass.config_entries.async_get_entry(entry_id)
            if entry is None:
                _LOGGER.debug(
                    "MQTT token yenilendi ama entry (%s) artık mevcut "
                    "değil (muhtemelen kaldırılmış/reload olmuş) — "
                    "atlanıyor.", entry_id,
                )
                return
            existing = entry.data.get(CONF_SHARING_TOKEN_INFO, {}) or {}
            merged = {**existing, **token_info}
            _LOGGER.debug(
                "MQTT token güncelleniyor. Gelen alanlar: %s, önceki "
                "alanlar: %s, sonuçtaki alanlar: %s",
                list(token_info.keys()), list(existing.keys()), list(merged.keys()),
            )
            new_data = {**entry.data, CONF_SHARING_TOKEN_INFO: merged}
            # Bu sadece token persist'i — kullanıcı ayarı değişmedi,
            # entegrasyonun reload olmasına gerek yok. __init__.py'deki
            # add_update_listener'ın bunu tetiklememesi için bayrağı
            # önceden set ediyoruz (bkz. coordinator.skip_next_reload).
            coordinator.skip_next_reload = True
            # Veri gerçekten değişmediyse HA güncelleme dinleyicisini HİÇ
            # çağırmaz; bayrak takılı kalıp bir sonraki GERÇEK ayar
            # değişikliğinin yutulmasına yol açardı.
            if not hass.config_entries.async_update_entry(entry, data=new_data):
                coordinator.skip_next_reload = False

        class _Impl(SharingTokenListener):
            def update_token(self, token_info: dict) -> None:
                hass.loop.call_soon_threadsafe(_persist, token_info)

        return _Impl()
