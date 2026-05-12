"""Select platform for Tuya Heatpump."""
from __future__ import annotations
import logging
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .conversion import Conversion
from .coordinator import TuyaScaleDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Tuya Heatpump selects from a config entry."""
    coordinator: TuyaScaleDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    selects = []
    
    select_configs = coordinator.model_mapping.get("selects", {})
    
    for select_code, select_config in select_configs.items():
        selects.append(
            TuyaHeatpumpSelect(coordinator, select_code, select_config)
        )
        _LOGGER.info(
            "Adding select: %s (%s)",
            select_config.get('name', select_code),
            select_code
        )
    
    async_add_entities(selects)


class TuyaHeatpumpSelect(SelectEntity):
    """Representation of a Tuya Heatpump Select."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        select_code: str,
        config: dict
    ) -> None:
        """Initialize the select."""
        self.coordinator = coordinator
        self._select_code = select_code
        self._config = config
        
        # Device name ile unique_id oluştur
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_{select_code}"
        
        # Translation key varsa kullan
        if 'translation_key' in config:
            self._attr_translation_key = config['translation_key']
        else:
            self._attr_name = config.get('name', select_code)
        
        self._attr_icon = config.get('icon')
        
        # Options'ları config'den al
        options_dict = config.get('options', {})
        if isinstance(options_dict, dict):
            self._attr_options = list(options_dict.keys())
            self._option_labels = options_dict
        else:
            self._attr_options = options_dict
            self._option_labels = {opt: opt for opt in options_dict}
        
        # Device info
        self._attr_device_info = coordinator.device_info

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        if not self.coordinator.data or self._select_code not in self.coordinator.data:
            return None
            
        raw_value = self.coordinator.data[self._select_code]['value']
        
        conversion = Conversion(self._config.get('conversion', 'value'))
        try:
            value = conversion.convert(raw_value)
        except Exception as err:
            value = raw_value
            _LOGGER.warning("Conversion failed for %s: %s", self._select_code, err)

        if isinstance(value, str):
            return value
        
        _LOGGER.warning("Unexpected value type for %s: %s", self._select_code, type(value))
        return None

    @property
    def options(self) -> list[str]:
        """Return a list of available options."""
        return self._attr_options

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Tuya DP ID ve Code bilgilerini attributes'a ekle."""
        attrs: dict[str, Any] = {}
        
        dp_info = self.coordinator.get_tuya_dp_info(self._select_code)
        attrs["tuya_code"] = dp_info["code"]
        attrs["tuya_dp_id"] = dp_info["dp_id"]

        if self.coordinator.model_id:
            attrs["tuya_model_id"] = self.coordinator.model_id

        # Select için values bilgisi faydalı olur
        if self._config and isinstance(self._config, dict) and "values" in self._config:
            attrs["tuya_values"] = self._config["values"]

        return attrs

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.info("Changing %s to %s", self._select_code, option)

        api_value = option
        if (api_conversion := self._config.get('api_conversion')) is not None:
            conversion = Conversion(api_conversion)
            try:
                api_value = conversion.convert(option)
                _LOGGER.debug("Converted HA option %s → API value %s", option, api_value)
            except Exception as err:
                _LOGGER.warning("API conversion failed: %s", err)
        
        success = await self.coordinator.send_command(self._select_code, api_value)
        
        if success:
            _LOGGER.info("✅ Successfully changed %s to %s", self._select_code, option)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.warning("❌ Failed to change %s to %s", self._select_code, option)
            raise HomeAssistantError(
                f"{self._config.get('name', self._select_code)} cannot be changed. "
                f"Your device does not allow changing this mode."
            )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and 
            self.coordinator.data is not None and
            self._select_code in self.coordinator.data
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
