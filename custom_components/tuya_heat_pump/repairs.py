"""Repair flows for Tuya Heat Pump.

Şu an tek bir onarım akışı var: MQTT (tuya_sharing) token'ı bozulur/
eksik kalırsa (bkz. sharing_mqtt.py'nin async_start()'ı), kullanıcıya
Ayarlar -> Sistem -> Onarımlar sayfasında tıklanabilir bir "Fix"
bildirimi çıkar. Tıklayınca aynı QR onay akışı (config_flow.py'deki
cloud_qr adımıyla birebir aynı mantık, SharingQRLogin üzerinden)
tekrar gösterilir.

Bu dosya sadece token bozulduğunda devreye giriyor — normal, sağlıklı
kurulumlarda hiç kullanılmıyor.
"""
from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant.components.repairs import RepairsFlow
from homeassistant.core import HomeAssistant
from homeassistant.helpers import selector

from .const import CONF_SHARING_TOKEN_INFO, CONF_USER_CODE
from .sharing_mqtt import SharingQRLogin

_LOGGER = logging.getLogger(__name__)

ISSUE_ID_TOKEN_INVALID = "mqtt_token_invalid"


class MqttReauthRepairFlow(RepairsFlow):
    """MQTT token'ı bozulmuş/eksikse kullanıcıdan tekrar QR onayı ister."""

    def __init__(self, hass: HomeAssistant, entry_id: str) -> None:
        self._hass = hass
        self._entry_id = entry_id
        self._qr_login: SharingQRLogin | None = None

    async def async_step_init(self, user_input=None):
        return await self.async_step_confirm()

    async def async_step_confirm(self, user_input=None):
        errors = {}
        entry = self._hass.config_entries.async_get_entry(self._entry_id)
        if entry is None:
            return self.async_abort(reason="entry_not_found")

        user_code = entry.data.get(CONF_USER_CODE)
        if not user_code:
            return self.async_abort(reason="no_user_code")

        if self._qr_login is None:
            self._qr_login = SharingQRLogin(self._hass)

        if user_input is not None:
            # Kullanici "Submit" bastiginda buraya dusuyoruz - QR'i
            # onaylamis mi kontrol ediyoruz.
            success, token_info = await self._qr_login.async_check_login(user_code)
            if success and token_info:
                new_data = {**entry.data, CONF_SHARING_TOKEN_INFO: token_info}
                self._hass.config_entries.async_update_entry(entry, data=new_data)
                await self._hass.config_entries.async_reload(entry.entry_id)
                return self.async_create_entry(title="", data={})
            errors["base"] = "qr_not_confirmed"

        # Ilk gosterimde (ya da basarisiz onay sonrasi tekrar) yeni QR iste.
        qr_response = await self._qr_login.async_request_qr(user_code)
        if not qr_response.get("success"):
            _LOGGER.warning("Onarım akışı: QR kod isteği başarısız: %s", qr_response)
            errors["base"] = "qr_request_failed"
            schema = vol.Schema({})
        else:
            schema = vol.Schema(
                {
                    vol.Optional("qr"): selector.QrCodeSelector(
                        config=selector.QrCodeSelectorConfig(
                            data=self._qr_login.qr_token,
                            scale=5,
                            error_correction_level=selector.QrErrorCorrectionLevel.QUARTILE,
                        )
                    )
                }
            )

        return self.async_show_form(
            step_id="confirm",
            data_schema=schema,
            errors=errors,
        )


async def async_create_fix_flow(hass: HomeAssistant, issue_id: str, data: dict | None):
    """HA'nın Repairs sistemi, kullanıcı "Fix" butonuna basınca bunu çağırır."""
    entry_id = data.get("entry_id") if data else None
    return MqttReauthRepairFlow(hass, entry_id)
