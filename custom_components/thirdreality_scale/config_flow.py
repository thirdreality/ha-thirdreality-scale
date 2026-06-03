"""Config flow for ThirdReality Smart Scale integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_PLATFORM,
    CONF_Z2M_TOPIC,
    CONF_ZHA_IEEE,
    CONF_FEATURES,
    CONF_TTS_SPEAKER,
    CONF_TTS_ENGINE,
    PLATFORM_Z2M,
    PLATFORM_ZHA,
    FEATURE_COCKTAIL,
    FEATURE_CALORIE,
    DEFAULT_TTS_ENGINE,
)


class ThirdRealityScaleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ThirdReality Smart Scale."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._data: dict = {}

    async def async_step_user(self, user_input=None):
        """Step 1: Select platform and device."""
        errors = {}

        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_features()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PLATFORM, default=PLATFORM_Z2M): vol.In(
                        {PLATFORM_Z2M: "Zigbee2MQTT", PLATFORM_ZHA: "ZHA"}
                    ),
                    vol.Optional(CONF_Z2M_TOPIC, default=""): str,
                    vol.Optional(CONF_ZHA_IEEE, default=""): str,
                }
            ),
            errors=errors,
        )

    async def async_step_features(self, user_input=None):
        """Step 2: Select features to enable."""
        errors = {}

        if user_input is not None:
            self._data[CONF_FEATURES] = user_input.get(CONF_FEATURES, [])
            return await self.async_step_voice()

        return self.async_show_form(
            step_id="features",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_FEATURES, default=[FEATURE_COCKTAIL, FEATURE_CALORIE]): 
                        selector.SelectSelector(
                            selector.SelectSelectorConfig(
                                options=[
                                    selector.SelectOptionDict(value=FEATURE_COCKTAIL, label="🍸 Cocktail Mixing Assistant"),
                                    selector.SelectOptionDict(value=FEATURE_CALORIE, label="🔥 Calorie Tracker"),
                                ],
                                multiple=True,
                            )
                        ),
                }
            ),
            errors=errors,
        )

    async def async_step_voice(self, user_input=None):
        """Step 3: Configure voice announcements (optional)."""
        errors = {}

        if user_input is not None:
            self._data.update(user_input)
            # 创建配置条目
            title = f"ThirdReality Scale ({self._data.get(CONF_Z2M_TOPIC) or self._data.get(CONF_ZHA_IEEE) or 'Unknown'})"
            return self.async_create_entry(title=title, data=self._data)

        return self.async_show_form(
            step_id="voice",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_TTS_ENGINE, default=DEFAULT_TTS_ENGINE): str,
                    vol.Optional(CONF_TTS_SPEAKER, default=""): str,
                }
            ),
            errors=errors,
        )
