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
from typing import Any, Dict, Optional

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
    ERROR_AUTH,
    ERROR_CONN,
    DEFAULT_NAME,
    DEFAULT_MANUFACTURER,
    DEFAULT_MODEL,
    DEVICE_MAPPINGS,
    FALLBACK_MODEL,
    VALUE_SCALING,
    CALCULATED_FIELDS,
)

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
        scan_interval = timedelta(
            minutes=config_entry.options.get(
                CONF_SCAN_INTERVAL,
                config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
            )
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=scan_interval,
        )
        
        self.access_id = config_entry.data[CONF_ACCESS_ID]
        self.access_key = config_entry.data[CONF_ACCESS_KEY]
        self.device_id = config_entry.data[CONF_DEVICE_ID]
        self.region = config_entry.data[CONF_REGION]
        self.api_endpoint = REGIONS[self.region]
        self.access_token = None
        self.device_name = DEFAULT_NAME
        self.is_online = True
        self.device_model = None
        self.device_mapping = None
        self.value_scaling = None

        # Geçici device info
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, self.device_id)},
            name=self.device_name,
            manufacturer=DEFAULT_MANUFACTURER,
            model=DEFAULT_MODEL,
        )

    async def get_device_info(self) -> dict:
        """Get device information from Tuya API."""
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
                self.device_model = device_data.get('model', 'unknown')
                
                _LOGGER.info("Device name: %s, Model: %s", self.device_name, self.device_model)
                
                # Device mapping'i belirle
                if self.device_model in DEVICE_MAPPINGS:
                    self.device_mapping = DEVICE_MAPPINGS[self.device_model]
                    _LOGGER.info("Using device mapping for model: %s", self.device_model)
                else:
                    self.device_mapping = DEVICE_MAPPINGS[FALLBACK_MODEL]
                    _LOGGER.warning("Unknown device model %s, using fallback mapping", self.device_model)
                
                # Value scaling'i belirle
                if self.device_model in VALUE_SCALING:
                    self.value_scaling = VALUE_SCALING[self.device_model]
                else:
                    self.value_scaling = VALUE_SCALING[FALLBACK_MODEL]
                
                # Device info'yu güncelle
                self.device_info = DeviceInfo(
                    identifiers={(DOMAIN, self.device_id)},
                    name=self.device_name,
                    manufacturer=DEFAULT_MANUFACTURER,
                    model=product_name,
                    model_id=self.device_model,
                )
                return device_data
            else:
                _LOGGER.warning("Failed to get device info, using defaults")
                # Fallback mapping kullan
                self.device_mapping = DEVICE_MAPPINGS[FALLBACK_MODEL]
                self.value_scaling = VALUE_SCALING[FALLBACK_MODEL]
                return {}
                
        except Exception as err:
            _LOGGER.error("Error getting device info: %s", str(err))
            # Fallback mapping kullan
            self.device_mapping = DEVICE_MAPPINGS[FALLBACK_MODEL]
            self.value_scaling = VALUE_SCALING[FALLBACK_MODEL]
            return {}

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

    def _get_actual_dp_code(self, entity_type: str, entity_key: str) -> Optional[str]:
        """Get actual DP code for entity based on device mapping."""
        if not self.device_mapping:
            return None
        
        mapping = self.device_mapping.get(entity_type, {})
        return mapping.get(entity_key)

    def _scale_value(self, dp_code: str, value: Any) -> Any:
        """Scale value based on device model and DP code."""
        if not self.value_scaling or not isinstance(value, (int, float)):
            return value
        
        # Özel scaling kuralları
        if dp_code in ['cur_current', 'b_cur', 'c_cur']:
            return value * self.value_scaling.get('current', 1.0)
        elif dp_code in ['voltage_current', 'bv', 'cv']:
            return value * self.value_scaling.get('voltage', 1.0)
        elif dp_code in ['cur_power']:
            return value * self.value_scaling.get('power', 1.0)
        elif dp_code in ['electric_total', 'power_consumption']:
            return value * self.value_scaling.get('energy', 1.0)
        elif 'temp' in dp_code.lower():
            return value * self.value_scaling.get('temperature', 1.0)
        
        return value

    async def send_command(self, entity_type: str, entity_key: str, value) -> bool:
        """Send command to device."""
        try:
            if not self.access_token:
                await self._get_token()

            # Gerçek DP kodunu al
            actual_dp_code = self._get_actual_dp_code(entity_type, entity_key)
            if not actual_dp_code:
                _LOGGER.error("No DP mapping found for %s.%s", entity_type, entity_key)
                return False

            t = str(int(time.time() * 1000))
            path = DEVICE_COMMAND_PATH.format(device_id=self.device_id)
            
            # Ters scaling: kullanıcı değerini DP formatına çevir
            if entity_type == "numbers" and isinstance(value, (int, float)):
                # Number entity'leri için ters scaling
                if entity_key in ['heat_temp_set', 'hot_water_temp_set']:
                    # Sıcaklık değerlerini 10 ile çarp (API formatı)
                    value = int(value * 10)
            
            commands = {
                "commands": [
                    {
                        "code": actual_dp_code,
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
            
            _LOGGER.info("Sending command: %s = %s (DP: %s)", entity_key, value, actual_dp_code)
            
            response = await self.hass.async_add_executor_job(
                make_api_request,
                url,
                headers,
                "POST",
                commands
            )
            
            result = response.json()
            
            if result.get('success', False):
                _LOGGER.info("✅ Command successful: %s = %s", entity_key, value)
                await asyncio.sleep(2)
                await self.async_request_refresh()
                return True
            else:
                error_msg = result.get('msg', 'Unknown error')
                _LOGGER.error("❌ Command failed: %s = %s -> %s", entity_key, value, error_msg)
                return False
                
        except Exception as err:
            _LOGGER.error("Error sending command %s: %s", entity_key, str(err))
            return False

    def _calculate_power(self, data: Dict) -> Optional[float]:
        """Calculate power from voltage and current."""
        voltage = None
        current = None
        
        # Gerçek DP kodlarını bul
        voltage_dp = self._get_actual_dp_code("sensors", "ac_vol")
        current_dp = self._get_actual_dp_code("sensors", "ac_curr")
        
        if voltage_dp and voltage_dp in data:
            voltage = data[voltage_dp].get('value')
            voltage = self._scale_value(voltage_dp, voltage) if isinstance(voltage, (int, float)) else None
        
        if current_dp and current_dp in data:
            current = data[current_dp].get('value')
            current = self._scale_value(current_dp, current) if isinstance(current, (int, float)) else None
        
        if voltage is not None and current is not None:
            return round(voltage * current, 2)
        
        return None

    async def _async_update_data(self):
        """Fetch data from Tuya API."""
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
            
            # Ham datayı işle
            raw_data = {}
            for prop in properties:
                code = prop['code']
                value = prop['value']
                timestamp = prop.get('time', 0)
                value_type = prop.get('type', '')
                
                raw_data[code] = {
                    'value': value,
                    'timestamp': timestamp,
                    'type': value_type,
                    'last_update': datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                }
            
            # Mapping'e göre data oluştur
            processed_data = {}
            
            # Önce hesaplanan değerleri ekle
            if "calculated_power" in self.device_mapping.get("sensors", {}):
                power_value = self._calculate_power(raw_data)
                if power_value is not None:
                    processed_data["calculated_power"] = {
                        'value': power_value,
                        'timestamp': current_time,
                        'type': 'calculated',
                        'last_update': datetime.fromtimestamp(current_time / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    }
            
            # Tüm mapping'leri işle
            for entity_type in ["sensors", "binary_sensors", "switches", "numbers", "selects", "extra_sensors"]:
                mapping = self.device_mapping.get(entity_type, {})
                for entity_key, dp_code in mapping.items():
                    if dp_code == "__calculated__":
                        continue  # Hesaplanan değerler zaten eklendi
                    
                    if dp_code in raw_data:
                        raw_value = raw_data[dp_code]['value']
                        # Değeri scale et
                        scaled_value = self._scale_value(dp_code, raw_value)
                        
                        processed_data[entity_key] = {
                            'value': scaled_value,
                            'timestamp': raw_data[dp_code]['timestamp'],
                            'type': raw_data[dp_code]['type'],
                            'last_update': raw_data[dp_code]['last_update'],
                            'original_dp': dp_code,  # Debug için
                            'original_value': raw_value  # Debug için
                        }
            
            return processed_data
            
        except Exception as err:
            self.is_online = False
            _LOGGER.info("Device OFFLINE - exception: %s", err)
            raise UpdateFailed(f"Error: {str(err)}")
