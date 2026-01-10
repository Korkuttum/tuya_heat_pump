"""Select platform for Tuya Heatpump."""
from __future__ import annotations
import logging
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, SELECT_TYPES, EXTRA_SELECT_TYPES
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
    
    # Cihaz mapping'ini kontrol et
    if not coordinator.device_mapping:
        _LOGGER.error("Device mapping not found, cannot create selects")
        async_add_entities(selects)
        return
    
    device_model = coordinator.device_model or "unknown"
    
    # Ana select'leri ekle
    select_mapping = coordinator.device_mapping.get("selects", {})
    for select_key in SELECT_TYPES:
        if select_key in select_mapping:
            selects.append(TuyaHeatpumpSelect(coordinator, select_key, device_model))
            _LOGGER.info("Adding select: %s -> %s", select_key, select_mapping[select_key])
        else:
            _LOGGER.debug("Select %s not in device mapping, skipping", select_key)
    
    # Ekstra select'leri ekle (yeni cihaz için)
    extra_select_mapping = coordinator.device_mapping.get("extra_selects", {})
    for select_key, dp_code in extra_select_mapping.items():
        if select_key in EXTRA_SELECT_TYPES:
            # Bu select sadece desteklenen modellerde mi kontrol et
            supported_models = EXTRA_SELECT_TYPES[select_key].get("supported_models", [])
            if device_model in supported_models:
                selects.append(TuyaHeatpumpExtraSelect(coordinator, select_key))
                _LOGGER.info("Adding extra select: %s -> %s", select_key, dp_code)
            else:
                _LOGGER.debug("Extra select %s not supported for model %s", select_key, device_model)
        else:
            _LOGGER.debug("Extra select %s not defined", select_key)
    
    async_add_entities(selects)

class TuyaHeatpumpSelect(SelectEntity):
    """Representation of a Tuya Heatpump Select."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        select_key: str,
        device_model: str
    ) -> None:
        """Initialize the select."""
        self.coordinator = coordinator
        self._select_key = select_key
        self._device_model = device_model
        self._select_config = SELECT_TYPES.get(select_key, {})
        
        # Device name ile unique_id oluştur
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_{select_key}"
        
        self._attr_name = self._select_config.get('name', select_key)
        self._attr_icon = self._select_config.get('icon')
        
        # Model'e göre options'ları belirle
        options_key = f"options_model_{device_model}"
        if options_key in self._select_config:
            self._attr_options = list(self._select_config[options_key].keys())
            self._options_map = self._select_config[options_key]
        else:
            # Fallback: ilk options setini kullan
            for key in self._select_config:
                if key.startswith("options_model_"):
                    self._attr_options = list(self._select_config[key].keys())
                    self._options_map = self._select_config[key]
                    break
            else:
                self._attr_options = []
                self._options_map = {}
        
        # Device info
        self._attr_device_info = coordinator.device_info

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        if not self.coordinator.data or self._select_key not in self.coordinator.data:
            return None
            
        value_data = self.coordinator.data[self._select_key]
        value = value_data.get('value')
        
        if isinstance(value, str):
            # Değeri options map'te ara
            for option_key, option_value in self._options_map.items():
                if option_key == value or option_value == value:
                    return option_key
            # Bulamazsak value'yu direkt döndür
            return value
        
        _LOGGER.warning("Unexpected value type for %s: %s", self._select_key, type(value))
        return None

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra state attributes."""
        if not self.coordinator.data or self._select_key not in self.coordinator.data:
            return {}
            
        attrs = {}
        value_data = self.coordinator.data[self._select_key]
        
        if 'last_update' in value_data:
            attrs['last_update'] = value_data['last_update']
        if 'original_dp' in value_data:
            attrs['dp_code'] = value_data['original_dp']
        
        return attrs

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.info("Changing %s to %s", self._select_key, option)
        
        # Option'ı API formatına çevir
        api_value = self._options_map.get(option, option)
        
        success = await self.coordinator.send_command("selects", self._select_key, api_value)
        
        if success:
            _LOGGER.info("✅ Successfully changed %s to %s", self._select_key, option)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.warning("❌ Failed to change %s to %s", self._select_key, option)
            raise HomeAssistantError(
                f"{self._select_config.get('name', self._select_key)} değiştirilemiyor. "
                f"Cihazınız bu modu değiştirmeye izin vermiyor. "
                f"Lütfen modu cihaz üzerinden yapın."
            )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and 
            self.coordinator.data is not None and
            self._select_key in self.coordinator.data
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

class TuyaHeatpumpExtraSelect(SelectEntity):
    """Representation of an extra Tuya Heatpump Select (for new device)."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        select_key: str
    ) -> None:
        """Initialize the extra select."""
        self.coordinator = coordinator
        self._select_key = select_key
        self._select_config = EXTRA_SELECT_TYPES.get(select_key, {})
        
        # Device name ile unique_id oluştur
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_{select_key}"
        
        self._attr_name = self._select_config.get('name', select_key)
        self._attr_icon = self._select_config.get('icon')
        self._attr_options = list(self._select_config.get('options', {}).keys())
        self._options_map = self._select_config.get('options', {})
        
        # Device info
        self._attr_device_info = coordinator.device_info

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        if not self.coordinator.data or self._select_key not in self.coordinator.data:
            return None
            
        value_data = self.coordinator.data[self._select_key]
        value = value_data.get('value')
        
        if isinstance(value, str):
            # Değeri options map'te ara
            for option_key, option_value in self._options_map.items():
                if option_key == value or option_value == value:
                    return option_key
            return value
        
        return None

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra state attributes."""
        if not self.coordinator.data or self._select_key not in self.coordinator.data:
            return {}
            
        attrs = {}
        value_data = self.coordinator.data[self._select_key]
        
        if 'last_update' in value_data:
            attrs['last_update'] = value_data['last_update']
        if 'original_dp' in value_data:
            attrs['dp_code'] = value_data['original_dp']
        
        return attrs

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.info("Changing %s to %s", self._select_key, option)
        
        api_value = self._options_map.get(option, option)
        success = await self.coordinator.send_command("extra_selects", self._select_key, api_value)
        
        if success:
            _LOGGER.info("✅ Successfully changed %s to %s", self._select_key, option)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.warning("❌ Failed to change %s to %s", self._select_key, option)
            raise HomeAssistantError(
                f"{self._select_config.get('name', self._select_key)} değiştirilemiyor. "
                f"Lütfen ayarı cihaz üzerinden yapın."
            )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and 
            self.coordinator.data is not None and
            self._select_key in self.coordinator.data
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
