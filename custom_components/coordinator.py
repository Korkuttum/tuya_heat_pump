"""DataUpdateCoordinator for Tuya Scale."""
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

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    CONF_SCAN_INTERVAL,
    REGIONS,
    TOKEN_PATH,
    DEVICE_DATA_PATH,
    CONF_ACCESS_ID,
    CONF_ACCESS_KEY,
    CONF_DEVICE_ID,
    CONF_REGION,
    ERROR_AUTH,
    ERROR_CONN,
)

_LOGGER = logging.getLogger(__name__)

def make_api_request(url: str, headers: dict) -> requests.Response:
    """Make API request."""
    _LOGGER.debug("Making API request to %s with headers %s", url, headers)
    return requests.get(url, headers=headers)

class TuyaScaleDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Tuya Scale data."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        # Tarama aralığını yapılandırmadan al
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
            update_method=self._async_update_with_retry
        )
        
        self.access_id = config_entry.data[CONF_ACCESS_ID]
        self.access_key = config_entry.data[CONF_ACCESS_KEY]
        self.device_id = config_entry.data[CONF_DEVICE_ID]
        self.region = config_entry.data[CONF_REGION]
        self.api_endpoint = REGIONS[self.region]
        self.access_token = None
        self._retry_count = 0
        self._max_retries = 3

    def _calculate_sign(self, t: str, path: str, access_token: str = None) -> str:
        """Calculate signature for API requests."""
        # String to sign
        str_to_sign = []
        str_to_sign.append("GET")
        str_to_sign.append(hashlib.sha256(''.encode('utf8')).hexdigest())
        str_to_sign.append("")  # Empty headers
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
        
        _LOGGER.debug(
            "Signature calculation:\n"
            "String to sign: %s\n"
            "Message: %s\n"
            "Signature: %s",
            str_to_sign, message, signature
        )
        
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
            
            _LOGGER.debug(
                "Getting token\n"
                "URL: %s\n"
                "Headers: %s",
                url, json.dumps(headers, indent=2)
            )
            
            response = await self.hass.async_add_executor_job(
                make_api_request,
                url,
                headers
            )
            
            _LOGGER.debug("Token response: %s", response.text)
            
            if response.status_code != 200:
                _LOGGER.error(
                    "Token request failed\n"
                    "Status code: %s\n"
                    "Response: %s",
                    response.status_code, response.text
                )
                raise ConfigEntryAuthFailed(ERROR_AUTH)
            
            result = response.json()
            if not result.get('success', False):
                _LOGGER.error("Token request error: %s", result.get('msg'))
                raise ConfigEntryAuthFailed(ERROR_AUTH)
            
            self.access_token = result['result']['access_token']
            _LOGGER.debug("Got access token: %s", self.access_token)
            return True
            
        except requests.RequestException as err:
            _LOGGER.error("Connection error during token request: %s", str(err))
            raise UpdateFailed(ERROR_CONN)

    async def _async_update_with_retry(self):
        """Update data with retry mechanism."""
        try:
            self._retry_count = 0
            return await self._async_update_data()
        except UpdateFailed as err:
            self._retry_count += 1
            _LOGGER.warning(
                "Update failed (attempt %s of %s): %s",
                self._retry_count,
                self._max_retries,
                str(err)
            )
            
            if self._retry_count < self._max_retries:
                self.access_token = None
                await asyncio.sleep(2)  # Short wait before retry
                return await self._async_update_data()
            else:
                raise

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
            
            _LOGGER.debug(
                "Getting device data\n"
                "URL: %s\n"
                "Headers: %s",
                url, json.dumps(headers, indent=2)
            )
            
            response = await self.hass.async_add_executor_job(
                make_api_request,
                url,
                headers
            )
            
            _LOGGER.debug("Device data response: %s", response.text)
            
            if response.status_code == 401:
                _LOGGER.info("Token expired, refreshing...")
                self.access_token = None
                await self.async_refresh()
                return self.data
            
            if response.status_code != 200:
                raise UpdateFailed(f"HTTP error {response.status_code}")
            
            result = response.json()
            if not result.get('success', False):
                msg = result.get('msg', '')
                if 'token' in msg.lower():
                    _LOGGER.info("Token invalid, refreshing...")
                    self.access_token = None
                    await self.async_refresh()
                    return self.data
                raise UpdateFailed(f"API error: {msg}")
            
            data = {}
            properties = result.get('result', {}).get('properties', [])
            
            _LOGGER.debug("All properties received: %s", json.dumps(properties, indent=2))
            
            for prop in properties:
                code = prop['code']
                value = prop['value']
                timestamp = prop.get('time', 0)
                value_type = prop.get('type', '')
                
                _LOGGER.debug(
                    "Processing property:\n"
                    "Code: %s\n"
                    "Value: %s\n"
                    "Type: %s\n"
                    "Timestamp: %s",
                    code, value, value_type, timestamp
                )
                
                # Özel değer dönüşümleri
                if code == 'weight':
                    value = value / 1000  # Convert to kg
                elif code == 'battery':
                    value = bool(value)  # Convert to boolean
                elif code == 'time' and value_type == 'string':
                    # Eğer time değeri boşsa, timestamp'i kullan
                    if not value:
                        value = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                
                data[code] = {
                    'value': value,
                    'timestamp': timestamp,
                    'type': value_type,
                    'last_update': datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                }
                
                _LOGGER.debug("Processed data for %s: %s", code, data[code])
            
            _LOGGER.debug("Final processed data: %s", json.dumps(data, indent=2))
            return data
            
        except requests.RequestException as err:
            _LOGGER.error("Connection error: %s", str(err))
            self.access_token = None
            raise UpdateFailed(f"{ERROR_CONN}: {str(err)}")
        except Exception as err:
            _LOGGER.error("Unexpected error: %s", str(err))
            self.access_token = None
            raise UpdateFailed(f"Unexpected error: {str(err)}")
