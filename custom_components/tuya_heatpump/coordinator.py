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
    ERROR_AUTH,
    ERROR_CONN,
    DEFAULT_NAME,
    DEFAULT_MANUFACTURER,
    DEFAULT_MODEL,
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
        self._power_format = None  # Power'ın çalıştığı format

        # Device info
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, self.device_id)},
            name=DEFAULT_NAME,
            manufacturer=DEFAULT_MANUFACTURER,
            model=DEFAULT_MODEL,
        )

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

    async def send_command(self, code: str, value: bool) -> bool:
        """Send command to device."""
        try:
            if not self.access_token:
                await self._get_token()

            t = str(int(time.time() * 1000))
            path = DEVICE_COMMAND_PATH.format(device_id=self.device_id)
            
            # POWER İÇİN ÇALIŞAN FORMATI BUL
            if code == "switch" and self._power_format is None:
                _LOGGER.info("🔍 Finding working format for power switch...")
                found = await self._find_power_format(value)
                if found:
                    return True
                else:
                    _LOGGER.error("❌ No working format found for power!")
                    return False
            
            # POWER FORMATI BİLİNİYORSA, AYNI FORMATI DİĞER SWITCH'LER İÇİN KULLAN
            if self._power_format is not None:
                command_value = self._convert_value(value, self._power_format)
                success = await self._send_single_command(code, command_value)
                if success:
                    _LOGGER.info("✅ Command successful: %s = %s (using power format: %s)", code, command_value, self._power_format)
                    await asyncio.sleep(2)
                    await self.async_request_refresh()
                    return True
            
            # EĞER POWER FORMATI ÇALIŞMAZSA, TÜM FORMATLARI DENE
            _LOGGER.warning("Power format failed for %s, trying all formats", code)
            return await self._try_all_formats(code, value)
            
        except Exception as err:
            _LOGGER.error("Error sending command %s: %s", code, str(err))
            return False

    async def _find_power_format(self, value: bool) -> bool:
        """Find working format for power switch."""
        formats = [
            ("bool", value),
            ("int", 1 if value else 0),
            ("str_bool", str(value).lower()),
            ("str_int", "1" if value else "0"),
        ]
        
        for fmt_name, fmt_value in formats:
            success = await self._send_single_command("switch", fmt_value)
            if success:
                self._power_format = fmt_name
                _LOGGER.info("🎯 POWER working format found: %s -> %s", fmt_name, fmt_value)
                await asyncio.sleep(2)
                await self.async_request_refresh()
                return True
            else:
                _LOGGER.debug("Power format %s failed", fmt_name)
        
        return False

    async def _try_all_formats(self, code: str, value: bool) -> bool:
        """Try all formats for a switch."""
        formats = [
            ("bool", value),
            ("int", 1 if value else 0),
            ("str_bool", str(value).lower()),
            ("str_int", "1" if value else "0"),
            ("on_off", "on" if value else "off"),
            ("enable_disable", "enable" if value else "disable"),
        ]
        
        for fmt_name, fmt_value in formats:
            success = await self._send_single_command(code, fmt_value)
            if success:
                _LOGGER.info("✅ Command successful: %s = %s (format: %s)", code, fmt_value, fmt_name)
                await asyncio.sleep(2)
                await self.async_request_refresh()
                return True
            else:
                _LOGGER.debug("Format %s failed for %s", fmt_name, code)
        
        _LOGGER.error("🚫 ALL formats failed for %s", code)
        return False

    async def _send_single_command(self, code: str, value) -> bool:
        """Send a single command to device."""
        try:
            commands = {
                "commands": [
                    {
                        "code": code,
                        "value": value
                    }
                ]
            }
            
            body = json.dumps(commands)
            t = str(int(time.time() * 1000))
            path = DEVICE_COMMAND_PATH.format(device_id=self.device_id)
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
            
            _LOGGER.debug("Sending: %s = %s (%s)", code, value, type(value).__name__)
            
            response = await self.hass.async_add_executor_job(
                make_api_request,
                url,
                headers,
                "POST",
                commands
            )
            
            result = response.json()
            
            if result.get('success', False):
                _LOGGER.debug("✅ Command accepted: %s = %s", code, value)
                return True
            else:
                error_msg = result.get('msg', 'Unknown error')
                _LOGGER.debug("❌ Command failed: %s = %s -> %s", code, value, error_msg)
                return False
                
        except Exception as err:
            _LOGGER.error("Error in _send_single_command: %s", str(err))
            return False

    def _convert_value(self, value: bool, format_type: str):
        """Convert boolean value to specified format."""
        if format_type == "bool":
            return value
        elif format_type == "int":
            return 1 if value else 0
        elif format_type == "str_bool":
            return str(value).lower()
        elif format_type == "str_int":
            return "1" if value else "0"
        elif format_type == "on_off":
            return "on" if value else "off"
        elif format_type == "enable_disable":
            return "enable" if value else "disable"
        else:
            return value

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
            
            data = {}
            properties = result.get('result', {}).get('properties', [])
            
            # Switch değerlerini logla
            for prop in properties:
                code = prop['code']
                if code in ['switch', 'mute', 'holiday_sw']:
                    _LOGGER.info("📊 Switch %s: %s (%s)", code, prop['value'], type(prop['value']).__name__)
            
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
            _LOGGER.error("Error updating data: %s", str(err))
            self.access_token = None
            raise UpdateFailed(f"Error: {str(err)}")
