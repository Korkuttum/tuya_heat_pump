"""Config flow for Tuya Heat Pump integration."""
from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_ACCESS_ID,
    CONF_ACCESS_KEY,
    CONF_DEVICE_ID,
    CONF_REGION,
    CONF_SCAN_INTERVAL,
    CONF_CONNECTION_TYPE,
    CONF_IP,
    CONF_LOCAL_KEY,
    CONF_PROTOCOL,
    DEFAULT_SCAN_INTERVAL,
    REGIONS,
    DEFAULT_REGION,
    PROTOCOL_OPTIONS,
)
from .coordinator import TuyaScaleDataUpdateCoordinator  # ← Doğru sınıf adı, alias yok
import tinytuya

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ACCESS_ID): str,
        vol.Required(CONF_ACCESS_KEY): str,
        vol.Required(CONF_DEVICE_ID): str,
        vol.Required(CONF_REGION, default=DEFAULT_REGION): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=list(REGIONS.keys()),
                mode=selector.SelectSelectorMode.DROPDOWN
            )
        ),
        vol.Required(CONF_CONNECTION_TYPE, default="cloud"): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=["cloud", "local"],
                mode=selector.SelectSelectorMode.DROPDOWN
            )
        ),
    }
)

STEP_LOCAL_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP): str,
        vol.Required(CONF_LOCAL_KEY): str,
        vol.Required(CONF_PROTOCOL, default="3.4"): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=PROTOCOL_OPTIONS,
                mode=selector.SelectSelectorMode.DROPDOWN
            )
        ),
        # Scan interval kaldırıldı (localde sabit)
    }
)

STEP_CLOUD_OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Optional(
            CONF_SCAN_INTERVAL,
            default=DEFAULT_SCAN_INTERVAL
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=1,
                max=60,
                step=1,
                mode=selector.NumberSelectorMode.BOX
            )
        ),
    }
)

async def validate_input(hass: HomeAssistant, data: dict, connection_type: str) -> dict:
    """Validate the user input allows us to connect."""
    # Mock ConfigEntry oluştur (basit ve temiz şekilde)
    mock_config = type(
        "MockConfigEntry",
        (),
        {
            "data": data,
            "options": {
                CONF_SCAN_INTERVAL: data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
            },
        },
    )()

    if connection_type == "cloud":
        coordinator = TuyaScaleDataUpdateCoordinator(hass, mock_config)
        try:
            # Token ve device info almayı dene
            if not coordinator.access_token:
                await coordinator._get_token()
            await coordinator.get_device_info()
        except Exception as err:
            _LOGGER.error("Cloud validation error: %s", err)
            if "token" in str(err).lower() or "auth" in str(err).lower():
                raise InvalidAuth("Invalid credentials") from err
            raise CannotConnect("Cannot connect to Tuya cloud") from err

        return {"title": f"Tuya Heat Pump ({data[CONF_DEVICE_ID]})"}

    else:
        # Local validation
        try:
            device = tinytuya.Device(
                dev_id=data[CONF_DEVICE_ID],
                address=data[CONF_IP],
                local_key=data[CONF_LOCAL_KEY],
                version=float(data[CONF_PROTOCOL]),
            )
            status = await hass.async_add_executor_job(device.status)
            if not status or 'dps' not in status:
                raise CannotConnect("Failed to get device status")
        except Exception as err:
            _LOGGER.error("Local validation error: %s", err)
            raise CannotConnect(f"Cannot connect to local device: {err}") from err

        return {"title": f"Tuya Heat Pump Local ({data[CONF_DEVICE_ID]})"}


class TuyaHeatpumpOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self._config_entry.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        )
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=1,
                            max=60,
                            step=1,
                            mode=selector.NumberSelectorMode.BOX
                        )
                    ),
                }
            ),
        )


class TuyaHeatpumpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tuya Heat Pump."""

    VERSION = 1
    connection_type = None
    user_data = None  # Geçici user input sakla

    async def async_step_user(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            self.user_data = user_input
            self.connection_type = user_input[CONF_CONNECTION_TYPE]
            if self.connection_type == "cloud":
                return await self.async_step_cloud_options()
            else:
                return await self.async_step_local()

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_cloud_options(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            full_data = {**self.user_data, **user_input}
            try:
                info = await validate_input(self.hass, full_data, "cloud")
                await self.async_set_unique_id(full_data[CONF_DEVICE_ID])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info["title"], data=full_data)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="cloud_options", data_schema=STEP_CLOUD_OPTIONS_SCHEMA, errors=errors
        )

    async def async_step_local(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            full_data = {**self.user_data, **user_input}
            try:
                info = await validate_input(self.hass, full_data, "local")
                await self.async_set_unique_id(full_data[CONF_DEVICE_ID])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info["title"], data=full_data)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="local", data_schema=STEP_LOCAL_DATA_SCHEMA, errors=errors
        )

    @staticmethod
    @config_entries.HANDLERS.register(DOMAIN)
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return TuyaHeatpumpOptionsFlow(config_entry)


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
