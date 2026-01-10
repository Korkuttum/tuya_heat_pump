"""The Tuya Heatpump integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .coordinator import TuyaScaleDataUpdateCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Tuya Heatpump from a config entry."""
    coordinator = TuyaScaleDataUpdateCoordinator(hass, entry)
    
    # Önce device info'yu al (model ID'yi de alır)
    await coordinator.get_device_info()
    
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    entry.async_on_unload(entry.add_update_listener(async_update_options))
    
    return True

async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
