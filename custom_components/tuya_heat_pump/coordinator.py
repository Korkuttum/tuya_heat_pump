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

    def _calculate_sign(self, t: str, path: str, access_token: str = None, method: str = "GET", body: str = "") -> str:
        """Calculate signature for API requests."""
        # String to sign
        str_to_sign = []
        str_to_sign.append(method)
        str_to_sign.append(hashlib.sha256(body.encode('utf8') if body else ''.encode('utf8')).hexdigest())
        str_to_sign.append("")
        str_to_sign.append(path)
        str_to_sign = '\n'.join(str_to_sign)
        
        # Message
        message = self.access_id
        if access_token:
            message += access_token
        message += t + str_to_sign
        
        # Calculate signature
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
            # Local mode
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
                    
                    # Model mapping yükle
                    self.model_mapping = await async_load_model_mapping(self.hass, self.model_id)
                    
                    # dp_mapping oluştur
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
            # Local mode - default mapping kullan
            self.model_id = "default"
            self.model_mapping = await async_load_model_mapping(self.hass, self.model_id)
            
            # dp_mapping oluştur
            self.dp_mapping = {}
            for entity_type in ['sensors', 'binary_sensors', 'switches', 'numbers', 'selects']:
                for code, config in self.model_mapping.get(entity_type, {}).items():
                    if 'dp_id' in config:
                        dp_id = config['dp_id']
                        self.dp_mapping[dp_id] = code
            
            _LOGGER.info("Loaded default model mapping for local device with %d entities", len(self.dp_mapping))
            return {}

    async def send_command(self, code: str, value: Any) -> bool:
        """Send command to device."""
        try:
            if self.connection_type == "cloud":
                if not self.access_token:
                    await self._get_token()

                t = str(int(time.time() * 1000))
                path = DEVICE_COMMAND_PATH.format(device_id=self.device_id)
                
                # API conversion varsa uygula
                if self.model_mapping:
                    for entity_type in ['switches', 'numbers', 'selects']:
                        if code in self.model_mapping.get(entity_type, {}):
                            config = self.model_mapping[entity_type][code]
                            if 'api_conversion' in config:
                                api_value = eval(config['api_conversion'], {"value": value})
                                _LOGGER.debug("Converted %s → %s for API", value, api_value)
                                value = api_value
                            break
                
                commands = {
                    "commands": [
                        {
                            "code": code,
                            "value": value
                        }
                    ]
                }
                
                body = json.dumps(commands)
                sign = self._calculate_sign(t, path, self.access_token, "POST", body)
                
                headers = {
                    'client_id': self.access_id,
                    'access_token': self.access_token,
                    'sign': sign,
                    't': t,
                    'sign_method': 'HMAC-SHA256',
                    'Content-Type': 'application/json'
                }
                
                url = f"{self.api_endpoint}{path}"
                
                _LOGGER.info("Sending command: %s = %s", code, value)
                
                response = await self.hass.async_add_executor_job(
                    make_api_request,
                    url,
                    headers,
                    "POST",
                    commands
                )
                
                result = response.json()
                
                if result.get('success', False):
                    _LOGGER.info("✅ Command successful: %s = %s", code, value)
                    await asyncio.sleep(2)
                    await self.async_request_refresh()
                    return True
                else:
                    error_msg = result.get('msg', 'Unknown error')
                    _LOGGER.error("❌ Command failed: %s = %s -> %s", code, value, error_msg)
                    return False
                    
            else:
                # Local mode
                if not self.local_device:
                    _LOGGER.error("Local device not initialized")
                    return False
                    
                # code → dp_id dönüşümü
                dp_id = next((k for k, v in self.dp_mapping.items() if v == code), None)
                if dp_id is None:
                    _LOGGER.error("No dp_id mapping found for code: %s", code)
                    return False
                
                _LOGGER.info("Sending local command: dp %s (%s) = %s", dp_id, code, value)
                
                result = await self.hass.async_add_executor_job(
                    self.local_device.set_value, dp_id, value
                )
                
                if result:
                    _LOGGER.info("✅ Local command successful: dp %s = %s", dp_id, value)
                    await asyncio.sleep(1)
                    await self.async_request_refresh()
                    return True
                else:
                    _LOGGER.warning("❌ Local command failed for dp %s", dp_id)
                    return False
                    
        except Exception as err:
            _LOGGER.error("Error sending command %s: %s", code, str(err))
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
            # Local mode
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
