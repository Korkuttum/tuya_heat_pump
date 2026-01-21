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
    """Class to manage fetching Tuya Heatpump data."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.connection_type = config_entry.data.get(CONF_CONNECTION_TYPE, "cloud")

        if self.connection_type == "cloud":
            scan_interval = timedelta(
                minutes=config_entry.options.get(
                    CONF_SCAN_INTERVAL,
                    config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
                )
            )
        else:
            scan_interval = timedelta(seconds=30)

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
                self.local_device = tinytuya.Device(
                    dev_id=self.device_id,
                    address=self.ip,
                    local_key=self.local_key,
                    version=self.protocol,
                    persist=False
                )
                _LOGGER.info("Local Tuya device initialized: %s (protocol %.1f)", self.device_id, self.protocol)
            except Exception as err:
                _LOGGER.error("Failed to initialize TinyTuya device: %s", err)
                self.local_device = None

    def _calculate_sign(self, t: str, path: str, access_token: str = "") -> str:
        sign_str = self.access_id + access_token + t + path
        return hmac.new(
            self.access_key.encode('utf-8'),
            sign_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest().upper()

    async def _get_token(self) -> None:
        if self.connection_type != "cloud":
            return
        t = str(int(time.time() * 1000))
        path = TOKEN_PATH
        sign = self._calculate_sign(t, path)
        headers = {
            'client_id': self.access_id,
            'sign': sign,
            't': t,
            'sign_method': 'HMAC-SHA256',
        }
        url = f"{self.api_endpoint}{path}"
        response = await self.hass.async_add_executor_job(make_api_request, url, headers)
        if response.status_code != 200:
            raise ConfigEntryAuthFailed(ERROR_CONN)
        result = response.json()
        if not result.get('success'):
            raise ConfigEntryAuthFailed(ERROR_AUTH)
        self.access_token = result['result']['access_token']
        _LOGGER.debug("Access token refreshed")

    async def get_device_info(self) -> dict:
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
                response = await self.hass.async_add_executor_job(make_api_request, url, headers)
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        dev = result['result']
                        self.device_name = dev.get('name', DEFAULT_NAME)
                        self.model_id = dev.get('model', DEFAULT_MODEL)
                        self.device_info = DeviceInfo(
                            identifiers={(DOMAIN, self.device_id)},
                            name=self.device_name,
                            manufacturer=dev.get('manufacturer_name', DEFAULT_MANUFACTURER),
                            model=self.model_id,
                            sw_version=dev.get('software_version'),
                        )
                        return dev
            except Exception as err:
                _LOGGER.warning("Could not fetch device info from cloud: %s", err)

        self.model_id = "default"
        self.device_name = "Tuya Heat Pump (Local)"
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, self.device_id)},
            name=self.device_name,
            manufacturer=DEFAULT_MANUFACTURER,
            model=self.model_id,
        )
        return {}

    async def get_device_model(self) -> None:
        self.model_mapping = await async_load_model_mapping(self.hass, self.model_id)
        self.dp_mapping.clear()
        for category in ["sensors", "binary_sensors", "switches", "numbers", "selects"]:
            configs = self.model_mapping.get(category, {})
            for code, conf in configs.items():
                dp_id = conf.get("dp_id")
                if dp_id is not None:
                    self.dp_mapping[dp_id] = code
                    _LOGGER.debug("Mapped dp_id %s → code %s", dp_id, code)

    async def send_command(self, code: str, value: Any) -> bool:
        if self.connection_type == "cloud":
            if not self.access_token:
                await self._get_token()
            t = str(int(time.time() * 1000))
            path = DEVICE_COMMAND_PATH.format(device_id=self.device_id)
            sign = self._calculate_sign(t, path, self.access_token)
            headers = {
                'client_id': self.access_id,
                'access_token': self.access_token,
                'sign': sign,
                't': t,
                'sign_method': 'HMAC-SHA256',
                'Content-Type': 'application/json'
            }
            payload = {"commands": [{"code": code, "value": value}]}
            url = f"{self.api_endpoint}{path}"
            try:
                response = await self.hass.async_add_executor_job(
                    make_api_request, url, headers, "POST", payload
                )
                if response.status_code == 200:
                    result = response.json()
                    success = result.get('success', False)
                    if success:
                        _LOGGER.info("Cloud command sent: %s = %s", code, value)
                    else:
                        _LOGGER.warning("Cloud command failed: %s", result.get('msg'))
                    return success
                return False
            except Exception as err:
                _LOGGER.error("Error sending command %s: %s", code, str(err))
                return False
        else:
            if not self.local_device:
                _LOGGER.error("Local device not initialized")
                return False
            dp_id = next((k for k, v in self.dp_mapping.items() if v == code), None)
            if dp_id is None:
                _LOGGER.error("No dp_id mapping found for code: %s", code)
                return False
            try:
                success = await self.hass.async_add_executor_job(
                    self.local_device.set_value, dp_id, value
                )
                if success:
                    _LOGGER.info("Local command sent: dp %s (%s) = %s", dp_id, code, value)
                else:
                    _LOGGER.warning("Local command failed for dp %s", dp_id)
                return bool(success)
            except Exception as err:
                _LOGGER.error("Error sending local command dp %s: %s", dp_id, err)
                return False

    async def _async_update_data(self):
        """Fetch data from Tuya API or local device."""
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
                    _LOGGER.debug("Token expired, refreshing...")
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
                
                # ONLINE/OFFLINE tespiti
                current_time = int(time.time() * 1000)
                properties = result.get('result', {}).get('properties', [])
                
                if properties:
                    latest_timestamp = max(prop.get('time', 0) for prop in properties)
                    time_diff = current_time - latest_timestamp
                    
                    scan_interval_ms = self.update_interval.total_seconds() * 1000
                    tolerance_ms = scan_interval_ms + (60 * 1000)
                    
                    if time_diff > tolerance_ms:
                        self.is_online = False
                        _LOGGER.info("Device OFFLINE - data %s seconds old", time_diff // 1000)
                    else:
                        self.is_online = True
                        _LOGGER.debug("Device ONLINE - fresh data (%s seconds old)", time_diff // 1000)
                else:
                    self.is_online = False
                    _LOGGER.info("Device OFFLINE - no properties")
                
                data = {}
                for prop in properties:
                    code = prop['code']
                    value = prop['value']
                    timestamp = prop.get('time', 0)
                    value_type = prop.get('type', '')
                    
                    data[code] = {
                        'value': value,
                        'timestamp': timestamp,
                        'type': value_type,
                        'last_update': datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    }
                
                return data
                
            except Exception as err:
                self.is_online = False
                _LOGGER.info("Device OFFLINE - exception: %s", err)
                raise UpdateFailed(f"Error: {str(err)}")
        
        else:
            if not self.local_device:
                raise UpdateFailed("Local device not initialized")
            
            try:
                status = await self.hass.async_add_executor_job(self.local_device.status)
                if not status or 'dps' not in status:
                    self.is_online = False
                    raise UpdateFailed("No 'dps' in local status response")
                
                self.is_online = True
                data = {}
                current_ms = int(time.time() * 1000)
                current_str = datetime.fromtimestamp(current_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
                
                for dp_str, value in status['dps'].items():
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
                        _LOGGER.debug("Invalid dp_id in local response: %s", dp_str)
                
                if not data:
                    _LOGGER.warning("No known codes found in local DPS response")
                    self.is_online = False
                
                return data
            
            except Exception as err:
                self.is_online = False
                _LOGGER.info("Local device OFFLINE - exception: %s", err)
                raise UpdateFailed(f"Local error: {str(err)}")
