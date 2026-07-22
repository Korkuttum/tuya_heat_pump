"""The Tuya Heatpump integration."""
import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, PLATFORMS
from .coordinator import TuyaScaleDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

# get_device_info + get_device_model + ilk refresh için toplam üst sınır.
# Her adımın kendi içinde makul timeout'ları var (cloud istekleri 10sn,
# local status() ~7-8sn), ama HAOS açılışında ağ/DNS henüz tam hazır
# olmayabiliyor ve bunlar toplanabiliyor. Bu dış sınır, ne olursa olsun
# HA'nın açılışını (ya da bu entry'nin reload'unu) süresiz bekletmemesini
# garantiliyor — süre dolarsa ConfigEntryNotReady fırlatılır, HA bunu
# "biraz sonra tekrar dene" olarak ele alır (normal, beklenen davranış),
# boot akışını bloke eden asıl "sonsuza kadar takılı kalma" ihtimalini
# ortadan kaldırır.
SETUP_TIMEOUT = 25


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Tuya Heatpump from a config entry."""
    coordinator = TuyaScaleDataUpdateCoordinator(hass, entry)

    try:
        async with asyncio.timeout(SETUP_TIMEOUT):
            # Önce device info'yu al
            await coordinator.get_device_info()

            # Model bilgisini al
            await coordinator.get_device_model()

            await coordinator.async_config_entry_first_refresh()
    except asyncio.TimeoutError as err:
        raise ConfigEntryNotReady(
            f"Tuya Heat Pump setup timed out after {SETUP_TIMEOUT}s "
            f"(device_id={coordinator.device_id}) — will retry"
        ) from err

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # MQTT (tuya_sharing) — tamamen opsiyonel, bkz. sharing_mqtt.py.
    # Kullanıcı kurulumda User Code + QR onayı yapmadıysa (mevcut tüm
    # kurulumlar dahil) coordinator._async_start_mqtt() hiçbir şey
    # yapmadan hemen döner — davranış hiç değişmez. Model_mapping'in
    # kesin dolu olduğu (get_device_model + first_refresh tamamlandığı)
    # bu noktadan SONRA, arka planda (bloklamadan) başlatılıyor.
    hass.loop.create_task(coordinator._async_start_mqtt())

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
        coordinator: TuyaScaleDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
        if coordinator.sharing_mqtt is not None:
            await coordinator.sharing_mqtt.async_stop()
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
