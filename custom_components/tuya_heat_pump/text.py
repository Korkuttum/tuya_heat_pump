"""Text platform for Tuya Heatpump.

Covers whole-DP UTF-8 string fields (e.g. a coffee machine's username
slot) — the entire raw payload IS the value here, unlike the other
raw-field entities (switch/number/select) which each read/write a
single packed int at a byte offset inside a larger payload.
"""
from __future__ import annotations
import base64
import logging
from typing import Any

from homeassistant.components.text import TextEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .coordinator import TuyaScaleDataUpdateCoordinator
from .raw_codec import resolve_raw_source

_LOGGER = logging.getLogger(__name__)


def _decode_utf8_payload(b64_string: str | None) -> str | None:
    """Whole raw DP payload → UTF-8 string, trimmed at the first null
    byte (the device pads short strings with \\x00 to a fixed length)."""
    if not b64_string:
        return None
    try:
        raw_bytes = base64.b64decode(b64_string)
        return raw_bytes.split(b"\x00", 1)[0].decode("utf-8", errors="replace")
    except Exception as err:
        _LOGGER.debug("UTF-8 payload decode failed: %s", err)
        return None


def _encode_utf8_payload(value: str, max_length: int) -> str:
    """String → base64, UTF-8 encoded and null-padded/truncated to
    exactly max_length bytes (the DP's fixed payload size — Tuya raw
    DPs are fixed-length, so the byte count must match on every write)."""
    raw_bytes = value.encode("utf-8")[:max_length]
    raw_bytes = raw_bytes.ljust(max_length, b"\x00")
    return base64.b64encode(raw_bytes).decode("ascii")


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Tuya Heatpump text entities from a config entry."""
    coordinator: TuyaScaleDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    texts = []
    text_configs = coordinator.model_mapping.get("texts", {})

    for text_code, text_config in text_configs.items():
        raw_source = resolve_raw_source(coordinator, text_config)
        if raw_source and coordinator.data and raw_source in coordinator.data:
            text_config = {**text_config, "raw_source": raw_source}
            texts.append(TuyaHeatpumpText(coordinator, text_code, text_config))
            _LOGGER.info(
                "Adding text: %s (%s)",
                text_config.get('name', text_code),
                text_code
            )
        else:
            _LOGGER.debug(
                "Raw source for dp %s (text %s) not resolvable yet, skipping",
                text_config.get('dp_id'), text_code,
            )

    async_add_entities(texts)


class TuyaHeatpumpText(TextEntity):
    """Representation of a Tuya Heatpump whole-DP text field."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        text_code: str,
        config: dict
    ) -> None:
        """Initialize the text entity."""
        self.coordinator = coordinator
        self._text_code = text_code
        self._config = config

        # Device name ile unique_id oluştur
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_{text_code}"

        self._attr_name = config.get('name', text_code)
        self._attr_icon = config.get('icon')
        self._attr_native_min = 0
        # HA's text entity caps native_max at 255; clamp defensively in
        # case a model file specifies something larger.
        self._attr_native_max = min(config.get('max_length', 255), 255)
        self._attr_has_entity_name = True

        # Device info
        self._attr_device_info = coordinator.device_info

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info

    def _raw_source(self) -> str | None:
        return self._config.get("raw_source") or resolve_raw_source(self.coordinator, self._config)

    @property
    def native_value(self) -> str | None:
        """Return the current value."""
        raw_source = self._raw_source()
        if raw_source is None or not self.coordinator.data or raw_source not in self.coordinator.data:
            return None
        b64_value = self.coordinator.data[raw_source].get('value')
        return _decode_utf8_payload(b64_value)

    async def async_set_value(self, value: str) -> None:
        """Change the value."""
        _LOGGER.info("Attempting to set %s to %s", self._text_code, value)

        raw_source = self._raw_source()
        if raw_source is None:
            raise HomeAssistantError(
                f"{self._config.get('name', self._text_code)}: raw source not resolved yet"
            )

        max_length = self._config.get('max_length', 255)
        new_b64 = _encode_utf8_payload(value, max_length)
        success = await self.coordinator.send_command(raw_source, new_b64)

        if success:
            _LOGGER.info("✅ Successfully set %s to %s", self._text_code, value)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.warning("❌ Failed to set %s", self._text_code)
            raise HomeAssistantError(
                f"{self._config.get('name', self._text_code)} cannot be changed. "
                f"Your device does not allow changing this setting."
            )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Tuya DP ID ve Code bilgilerini attributes'a ekle."""
        attrs: dict[str, Any] = {}

        raw_source = self._raw_source()
        attrs["tuya_code"] = raw_source or "<unknown>"
        attrs["tuya_dp_id"] = self._config.get("dp_id")

        if self.coordinator.model_id:
            attrs["tuya_model_id"] = self.coordinator.model_id

        return attrs

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        raw_source = self._raw_source()
        return (
            self.coordinator.last_update_success and
            self.coordinator.data is not None and
            raw_source is not None and
            raw_source in self.coordinator.data
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
