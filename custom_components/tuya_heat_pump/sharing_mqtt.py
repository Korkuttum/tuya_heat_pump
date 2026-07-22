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
       - Hepsi mevcutsa -> bu cihaz için periyodik poll DURAKLATILIR,
         gelen push verisi doğrudan uygulanır.
       - Bir tanesi bile eksikse -> periyodik poll AYNEN DEVAM EDER,
         gelen push sadece "değişti, hemen tazele" tetikleyicisi
         olarak kullanılır (içeriğine bakılmaz).
  3. MQTT bağlantısı koparsa, periyodik poll otomatik olarak eski
     haline döner — hiçbir zaman veri akışı tamamen kesilmez.

Bu dosyadaki hiçbir şey, CONF_USER_CODE config_entry.data'da
tanımlanmadığı sürece devreye girmez — yani mevcut kurulumların
hiçbiri bundan etkilenmez.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from homeassistant.core import HomeAssistant

from .const import TUYA_SHARING_CLIENT_ID, TUYA_SHARING_SCHEMA

_LOGGER = logging.getLogger(__name__)


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

    @property
    def connected(self) -> bool:
        return self._connected

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

        try:
            listener = _PushDeviceListener(self)
            token_listener = _PersistTokenListener(self._hass, self._coordinator.config_entry)

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
            self._manager.add_device_listener(listener)

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

            self._sufficient = _device_covers_codes(
                device, _collect_required_codes(self._coordinator.model_mapping)
            )
            _LOGGER.info(
                "MQTT: cihaz %s için DP kapsama durumu: %s",
                self._coordinator.device_id,
                "yeterli (poll duraklatılacak)" if self._sufficient else "yetersiz (poll devam edecek, push sadece tetikleyici)",
            )

            await self._hass.async_add_executor_job(self._manager.refresh_mq)
            await asyncio.sleep(3)

            mq = getattr(self._manager, "mq", None)
            client = getattr(mq, "client", None) if mq else None
            if client is None:
                _LOGGER.warning("MQTT bağlantısı kurulamadı. Periyodik poll ile devam.")
                return False

            self._connected = True
            self._health_check_task = self._hass.loop.create_task(self._health_check_loop())
            return True

        except Exception as err:
            _LOGGER.warning("MQTT başlatılamadı (%s). Periyodik poll ile devam.", err)
            return False

    async def _health_check_loop(self) -> None:
        """Hafif, seyrek bir bağlantı kontrolü — agresif değil (bugün
        local modda öğrendiğimiz dersle tutarlı: sık kontrol gereksiz
        yük). Kopma tespit edilirse BİR KEZ yeniden bağlanmayı dener,
        olmazsa pes edip coordinator'a "MQTT yok" der."""
        while True:
            await asyncio.sleep(300)  # 5 dakikada bir kontrol
            mq = getattr(self._manager, "mq", None)
            client = getattr(mq, "client", None) if mq else None
            is_connected = bool(client and getattr(client, "is_connected", lambda: False)())

            if is_connected:
                self._reconnect_attempted = False
                continue

            if self._connected:
                _LOGGER.warning("MQTT bağlantısı koptu tespit edildi.")
                self._connected = False
                self._coordinator._mqtt_set_active(False)

            if not self._reconnect_attempted:
                self._reconnect_attempted = True
                _LOGGER.info("MQTT: bir kez yeniden bağlanma deneniyor...")
                try:
                    await self._hass.async_add_executor_job(self._manager.refresh_mq)
                    await asyncio.sleep(3)
                    mq = getattr(self._manager, "mq", None)
                    client = getattr(mq, "client", None) if mq else None
                    if client:
                        self._connected = True
                        self._coordinator._mqtt_set_active(True)
                        _LOGGER.info("MQTT: yeniden bağlanma başarılı.")
                except Exception as err:
                    _LOGGER.warning("MQTT: yeniden bağlanma denemesi başarısız (%s).", err)

    async def async_stop(self) -> None:
        if self._health_check_task:
            self._health_check_task.cancel()
        mq = getattr(self._manager, "mq", None) if self._manager else None
        stop = getattr(mq, "stop", None) if mq else None
        if callable(stop):
            try:
                await self._hass.async_add_executor_job(stop)
            except Exception:
                pass

    def _on_push(self, device, updated_status_properties: list[str]) -> None:
        """tuya_sharing'in ARKA PLAN THREAD'İNDEN çağrılıyor — HA event
        loop'una güvenli geçiş şart (call_soon_threadsafe /
        run_coroutine_threadsafe kullanmadan coordinator'a dokunmak
        thread-safety ihlali olur)."""
        if device.id != self._coordinator.device_id:
            return  # Manager tum hesabi dinliyor, bizi ilgilendirmeyen cihaz

        if self._sufficient:
            new_data = {
                code: {"value": device.status[code]}
                for code in updated_status_properties
                if code in device.status
            }
            if new_data:
                self._hass.loop.call_soon_threadsafe(
                    self._coordinator._mqtt_apply_push, new_data
                )
        else:
            asyncio.run_coroutine_threadsafe(
                self._coordinator._mqtt_trigger_refresh(), self._hass.loop
            )


class _PushDeviceListener:
    """tuya_sharing.SharingDeviceListener'ı burada import etmek yerine
    (modül yükleme sırasına bağımlılık oluşmasın diye) async_start()
    içinde dinamik import ediyoruz — bu sınıf onun somut halini
    çalışma zamanında oluşturuyor."""

    def __new__(cls, owner: "SharingMQTT"):
        from tuya_sharing import SharingDeviceListener

        class _Impl(SharingDeviceListener):
            def update_device(self, device, updated_status_properties=None, dp_timestamps=None) -> None:
                if updated_status_properties:
                    owner._on_push(device, updated_status_properties)

            def add_device(self, device) -> None:
                pass

            def remove_device(self, device_id: str) -> None:
                pass

        return _Impl()


class _PersistTokenListener:
    """Token yenilenince (tuya_sharing kendi içinde otomatik yapıyor)
    config_entry.data'ya kalıcı olarak yazar — yoksa HA her restart'ta
    kullanıcı tekrar QR okutmak zorunda kalır."""

    def __new__(cls, hass: HomeAssistant, config_entry):
        from tuya_sharing import SharingTokenListener
        from .const import CONF_SHARING_TOKEN_INFO

        def _persist(token_info: dict) -> None:
            new_data = {**config_entry.data, CONF_SHARING_TOKEN_INFO: token_info}
            hass.config_entries.async_update_entry(config_entry, data=new_data)

        class _Impl(SharingTokenListener):
            def update_token(self, token_info: dict) -> None:
                hass.loop.call_soon_threadsafe(_persist, token_info)

        return _Impl()
