"""DataUpdateCoordinator for Tuya Heatpump."""
from __future__ import annotations
import logging
import time
import hmac
import hashlib
import requests
import json
import asyncio
from datetime import datetime, timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    CONF_SCAN_INTERVAL,
    REGIONS,
    TOKEN_PATH,
    DEVICE_DATA_PATH,
    DEVICE_COMMAND_PATH,
    CONF_ACCESS_ID,
    CONF_ACCESS_KEY,
    CONF_DEVICE_ID,
    CONF_REGION,
    CONF_CONNECTION_TYPE,
    CONF_IP,
    CONF_LOCAL_KEY,
    CONF_PROTOCOL,
    ERROR_AUTH,
    ERROR_CONN,
    DEFAULT_NAME,
    DEFAULT_MANUFACTURER,
    DEFAULT_MODEL,
)
import tinytuya

from .model_loader import load_model_mapping, async_load_model_mapping

_LOGGER = logging.getLogger(__name__)

def make_api_request(url: str, headers: dict, method: str = "GET", data: dict = None) -> requests.Response:
    """Make API request."""
    try:
        if method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        else:
            response = requests.get(url, headers=headers, timeout=10)
        return response
    except requests.exceptions.Timeout:
        _LOGGER.error("Request timeout for %s", url)
        raise
    except requests.exceptions.RequestException as err:
        _LOGGER.error("Request error for %s: %s", url, err)
        raise


class TuyaScaleDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Tuya Heatpump data with Instant Updates."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.connection_type = config_entry.data.get(CONF_CONNECTION_TYPE, "cloud")
       
        # Cloud için poll devam eder, Local için anlık dinleme yapacağımızdan interval'i kapatıyoruz
        if self.connection_type == "cloud":
            scan_interval = timedelta(
                minutes=config_entry.options.get(
                    CONF_SCAN_INTERVAL,
                    config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
                )
            )
        else:
            # Local modda anlık güncelleme (push) kullanacağımız için periyodik sorgulamayı (poll) kapatıyoruz
            scan_interval = None

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=scan_interval,
        )
       
        self.config_entry = config_entry
        self.device_id = config_entry.data[CONF_DEVICE_ID]
        self.device_name = DEFAULT_NAME
        self.is_online = True
        self.model_id = None
        self.model_mapping = None
        self.dp_mapping = {}
        self._listener_task = None
        self._heartbeat_task = None

        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, self.device_id)},
            name=self.device_name,
            manufacturer=DEFAULT_MANUFACTURER,
            model=DEFAULT_MODEL,
        )

        if self.connection_type == "cloud":
            self.access_id = config_entry.data[CONF_ACCESS_ID]
            self.access_key = config_entry.data[CONF_ACCESS_KEY]
            self.region = config_entry.data[CONF_REGION]
            self.api_endpoint = REGIONS[self.region]
            self.access_token = None
        else:
            self.ip = config_entry.data[CONF_IP]
            self.local_key = config_entry.data[CONF_LOCAL_KEY]
            self.protocol = float(config_entry.data.get(CONF_PROTOCOL, "3.4"))
            try:
                # Persistent bağlantı aktif edildi
                self.local_device = tinytuya.Device(
                    dev_id=self.device_id,
                    address=self.ip,
                    local_key=self.local_key,
                    version=self.protocol,
                    persist=True
                )
                _LOGGER.info("Local Tuya device initialized (Persistent Mode): %s", self.device_id)
               
                # Dinleyici döngüsünü başlat
                self.hass.loop.create_task(self._async_start_listener())
               
            except Exception as err:
                _LOGGER.error("Failed to initialize TinyTuya device: %s", err)
                self.local_device = None

    async def _async_start_listener(self):
        """Start the background listener for instant updates."""
        _LOGGER.info("Starting TinyTuya listener loop for %s", self.device_id)
       
        # İlk veriyi bir kez çekelim
        await self.async_refresh()
       
        # Dinleme ve Heartbeat döngülerini başlat
        self._listener_task = self.hass.loop.create_task(self._listen_loop())
        self._heartbeat_task = self.hass.loop.create_task(self._heartbeat_loop())

    async def _listen_loop(self):
        """Loop to receive instant data from the device."""
        while True:
            try:
                # TinyTuya'nın receive() fonksiyonu bloklayıcıdır, executor ile çalıştırıyoruz
                data = await self.hass.async_add_executor_job(self.local_device.receive)
               
                if data and 'dps' in data:
                    _LOGGER.debug("Instant update received: %s", data['dps'])
                    new_data = self._process_local_dps(data['dps'])
                    if new_data:
                        # Coordinator içindeki veriyi güncelle ve entity'lere haber ver
                        self.async_set_updated_data(new_data)
               
                await asyncio.sleep(0.1) # CPU'yu yormamak için minik ara
            except Exception as err:
                _LOGGER.error("Error in listener loop: %s. Retrying in 5s...", err)
                await asyncio.sleep(5)

    async def _heartbeat_loop(self):
        """Loop to keep the connection alive."""
        while True:
            try:
                if self.local_device:
                    await self.hass.async_add_executor_job(self.local_device.heartbeat)
                await asyncio.sleep(15) # 15 saniyede bir heartbeat idealdir
            except Exception as err:
                _LOGGER.debug("Heartbeat error: %s", err)
                await asyncio.sleep(10)

    def _process_local_dps(self, dps: dict) -> dict:
        """Helper to convert raw DPS to our data format."""
        data = {}
        current_ms = int(time.time() * 1000)
        current_str = datetime.fromtimestamp(current_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
       
        for dp_str, value in dps.items():
            try:
                dp_id = int(dp_str)
                code = self.dp_mapping.get(dp_id)
                if code:
                    data[code] = {
                        'value': value,
                        'timestamp': current_ms,
                        'type': str(type(value).__name__),
                        'last_update': current_str
                    }
            except ValueError:
                continue
       
        # Eğer kısmi veri geldiyse, mevcut verilerle birleştir (coordinator.data)
        if self.data and isinstance(self.data, dict):
            updated_data = dict(self.data)
            updated_data.update(data)
            return updated_data
           
        return data

    def _calculate_sign(self, t: str, path: str, access_token: str = None, method: str = "GET", body: str = "") -> str:
        """Calculate signature for API requests."""
        str_to_sign = []
        str_to_sign.append(method)
        str_to_sign.append(hashlib.sha256(body.encode('utf8') if body else ''.encode('utf8')).hexdigest())
        str_to_sign.append("")
        str_to_sign.append(path)
        str_to_sign = '\n'.join(str_to_sign)
       
        message = self.access_id
        if access_token:
            message += access_token
        message += t + str_to_sign
       
        signature = hmac.new(
            self.access_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest().upper()
       
        return signature

    async def _get_token(self) -> bool:
        """Get access token from Tuya API."""
        if self.connection_type != "cloud":
            return True
           
        try:
            t = str(int(time.time() * 1000))
            sign = self._calculate_sign(t, TOKEN_PATH)
           
            headers = {
                'client_id': self.access_id,
                'sign': sign,
                't': t,
                'sign_method': 'HMAC-SHA256'
            }
           
            url = f"{self.api_endpoint}{TOKEN_PATH}"
           
            response = await self.hass.async_add_executor_job(
                make_api_request,
                url,
                headers
            )
           
            if response.status_code != 200:
                raise ConfigEntryAuthFailed(ERROR_AUTH)
           
            result = response.json()
            if not result.get('success', False):
                raise ConfigEntryAuthFailed(ERROR_AUTH)
           
            self.access_token = result['result']['access_token']
            _LOGGER.debug("Successfully got access token")
            return True
           
        except Exception as err:
            _LOGGER.error("Error getting token: %s", str(err))
            raise UpdateFailed(ERROR_CONN)

    async def get_device_info(self) -> dict:
        """Get device information."""
        if self.connection_type == "cloud":
            try:
                if not self.access_token:
                    await self._get_token()
                   
                t = str(int(time.time() * 1000))
                path = f"/v1.0/devices/{self.device_id}"
                sign = self._calculate_sign(t, path, self.access_token)
               
                headers = {
                    'client_id': self.access_id,
                    'access_token': self.access_token,
                    'sign': sign,
                    't': t,
                    'sign_method': 'HMAC-SHA256',
                }
               
                url = f"{self.api_endpoint}{path}"
                _LOGGER.info("Getting device info from API...")
               
                response = await self.hass.async_add_executor_job(
                    make_api_request,
                    url,
                    headers
                )
               
                result = response.json()
               
                if result.get('success', False):
                    device_data = result['result']
                    self.device_name = device_data.get('name', DEFAULT_NAME)
                    product_name = device_data.get('product_name', DEFAULT_MODEL)
                   
                    _LOGGER.info("Device name set to: %s", self.device_name)
                   
                    self.device_info = DeviceInfo(
                        identifiers={(DOMAIN, self.device_id)},
                        name=self.device_name,
                        manufacturer=DEFAULT_MANUFACTURER,
                        model=product_name,
                    )
                    return device_data
                else:
                    _LOGGER.warning("Failed to get device info, using default name: %s", DEFAULT_NAME)
                    return {}
                   
            except Exception as err:
                _LOGGER.error("Error getting device info: %s", str(err))
                return {}
        else:
            self.device_name = f"Tuya Heat Pump (Local) {self.device_id[-6:]}"
            self.device_info = DeviceInfo(
                identifiers={(DOMAIN, self.device_id)},
                name=self.device_name,
                manufacturer=DEFAULT_MANUFACTURER,
                model="Local Device",
            )
            return {}

    async def get_device_model(self) -> dict:
        """Get device model information."""
        if self.connection_type == "cloud":
            try:
                if not self.access_token:
                    await self._get_token()
                t = str(int(time.time() * 1000))
                path = f"/v2.0/cloud/thing/{self.device_id}/model"
                sign = self._calculate_sign(t, path, self.access_token)
               
                headers = {
                    'client_id': self.access_id,
                    'access_token': self.access_token,
                    'sign': sign,
                    't': t,
                    'sign_method': 'HMAC-SHA256',
                }
               
                url = f"{self.api_endpoint}{path}"
                _LOGGER.info("Getting device model from API...")
               
                response = await self.hass.async_add_executor_job(
                    make_api_request,
                    url,
                    headers
                )
               
                result = response.json()
               
                if result.get('success', False):
                    model_info = json.loads(result['result']['model'])
                    self.model_id = model_info.get('modelId')
                   
                    _LOGGER.info("Device model ID: %s", self.model_id)
                   
                    self.model_mapping = await async_load_model_mapping(self.hass, self.model_id)
                   
                    self.dp_mapping = {}
                    for entity_type in ['sensors', 'binary_sensors', 'switches', 'numbers', 'selects']:
                        for code, config in self.model_mapping.get(entity_type, {}).items():
                            if 'dp_id' in config:
                                dp_id = config['dp_id']
                                self.dp_mapping[dp_id] = code
                   
                    _LOGGER.info("Loaded model mapping with %d entities", len(self.dp_mapping))
                    return model_info
                else:
                    _LOGGER.warning("Failed to get device model, using default mapping")
                    self.model_mapping = load_model_mapping("default")
                    return {}
                   
            except Exception as err:
                _LOGGER.error("Error getting device model: %s", str(err))
                self.model_mapping = load_model_mapping("default")
                return {}
        else:
            self.model_id = "default"
            self.model_mapping = await async_load_model_mapping(self.hass, self.model_id)
           
            self.dp_mapping = {}
            for entity_type in ['sensors', 'binary_sensors', 'switches', 'numbers', 'selects']:
                for code, config in self.model_mapping.get(entity_type, {}).items():
                    if 'dp_id' in config:
                        dp_id = config['dp_id']
                        self.dp_mapping[dp_id] = code
           
            _LOGGER.info("Loaded default model mapping for local device with %d entities", len(self.dp_mapping))
            return {}

    async def send_command(self, code: str, value: Any) -> bool:
        """Send command to device - local mantığı gibi dönüşüm yapmadan ham gönderiyoruz"""
        try:
            if self.connection_type == "cloud":
                if not self.access_token:
                    await self._get_token()

                t = str(int(time.time() * 1000))
                path = DEVICE_COMMAND_PATH.format(device_id=self.device_id)
               
                original_value = value
                _LOGGER.debug("Cloud → Dönüşüm yapılmadan ham değer gönderiliyor: %s (orijinal HA değeri: %s)", value, original_value)

                # v2.0 formatı - ham value'yu gönder
                properties = {code: value}
                properties_json = json.dumps(properties)
                body_dict = {"properties": properties_json}
               
                body_str = json.dumps(body_dict)  # sign için
                sign = self._calculate_sign(t, path, self.access_token, "POST", body_str)
               
                headers = {
                    'client_id': self.access_id,
                    'access_token': self.access_token,
                    'sign': sign,
                    't': t,
                    'sign_method': 'HMAC-SHA256',
                    'Content-Type': 'application/json'
                }
               
                url = f"{self.api_endpoint}{path}"
                _LOGGER.info("Cloud komut (v2.0) - ham değer: %s = %s", code, value)
               
                response = await self.hass.async_add_executor_job(
                    make_api_request,
                    url,
                    headers,
                    "POST",
                    body_dict
                )
               
                result = response.json()
               
                if result.get('success', False):
                    _LOGGER.info("✅ Cloud komut başarılı: %s = %s", code, value)
                    await asyncio.sleep(2)
                    await self.async_request_refresh()
                    return True
                else:
                    error_msg = result.get('msg', 'Bilinmeyen hata')
                    _LOGGER.error("❌ Cloud komut başarısız: %s = %s → %s", code, value, error_msg)
                    return False
                   
            else:
                if not self.local_device:
                    _LOGGER.error("Local device not initialized")
                    return False
                   
                dp_id = next((k for k, v in self.dp_mapping.items() if v == code), None)
                if dp_id is None:
                    _LOGGER.error("No dp_id mapping found for code: %s", code)
                    return False
               
                _LOGGER.info("Local komut: dp %s (%s) = %s", dp_id, code, value)
               
                result = await self.hass.async_add_executor_job(
                    self.local_device.set_value, dp_id, value
                )
               
                if result:
                    _LOGGER.info("✅ Local komut başarılı: dp %s = %s", dp_id, value)
                    return True
                else:
                    _LOGGER.warning("❌ Local komut başarısız dp %s", dp_id)
                    return False
                   
        except Exception as err:
            _LOGGER.error("Error sending command %s: %s", code, str(err))
            return False

    async def _async_update_data(self):
        """Fetch data from Tuya API or local device (Manual Poll)."""
        if self.connection_type == "cloud":
            try:
                if not self.access_token:
                    await self._get_token()
                t = str(int(time.time() * 1000))
                path = DEVICE_DATA_PATH.format(device_id=self.device_id)
                sign = self._calculate_sign(t, path, self.access_token)
               
                headers = {
                    'client_id': self.access_id,
                    'access_token': self.access_token,
                    'sign': sign,
                    't': t,
                    'sign_method': 'HMAC-SHA256',
                }
               
                url = f"{self.api_endpoint}{path}"
               
                response = await self.hass.async_add_executor_job(
                    make_api_request,
                    url,
                    headers
                )
               
                if response.status_code == 401:
                    self.access_token = None
                    return await self._async_update_data()
               
                if response.status_code != 200:
                    raise UpdateFailed(f"HTTP error {response.status_code}")
               
                result = response.json()
                if not result.get('success', False):
                    msg = result.get('msg', '')
                    if 'token' in msg.lower():
                        self.access_token = None
                        return await self._async_update_data()
                    raise UpdateFailed(f"API error: {msg}")
               
                properties = result.get('result', {}).get('properties', [])
                data = {}
                for prop in properties:
                    code = prop['code']
                    data[code] = {
                        'value': prop['value'],
                        'timestamp': prop.get('time', 0),
                        'type': prop.get('type', ''),
                        'last_update': datetime.fromtimestamp(prop.get('time', 0) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    }
                return data
               
            except Exception as err:
                self.is_online = False
                raise UpdateFailed(f"Error: {str(err)}")
       
        else:
            # Local mode initial status fetch
            if not self.local_device:
                raise UpdateFailed("Local device not initialized")
           
            try:
                # Durumu zorla sorgula (sadece başlangıçta veya hata anında)
                status = await self.hass.async_add_executor_job(self.local_device.status)
               
                if not status or 'dps' not in status:
                    self.is_online = False
                    raise UpdateFailed("No 'dps' in local status response")
               
                self.is_online = True
                return self._process_local_dps(status['dps'])
           
            except Exception as err:
                self.is_online = False
                raise UpdateFailed(f"Local error: {str(err)}")
