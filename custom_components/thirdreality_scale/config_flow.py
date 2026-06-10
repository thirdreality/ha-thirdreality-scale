"""Config flow for ThirdReality Smart Scale integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import selector
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

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

Z2M_IDENTIFIER_PREFIX = "zigbee2mqtt_"
Z2M_BRIDGE_MARKER = "_bridge_"


def _build_z2m_options(hass: HomeAssistant) -> list[selector.SelectOptionDict]:
    """Build dropdown options for Zigbee2MQTT devices.

    Each option's value is the z2m topic (device friendly name), extracted
    from the MQTT device identifier by stripping the 'zigbee2mqtt_' prefix.
    The bridge device is skipped since it is not a scale.
    """
    dev_reg = dr.async_get(hass)
    options: list[selector.SelectOptionDict] = []
    for device in dev_reg.devices.values():
        for domain, ident in device.identifiers:
            if domain != "mqtt" or not ident.startswith(Z2M_IDENTIFIER_PREFIX):
                continue
            if Z2M_BRIDGE_MARKER in ident:
                continue
            topic = ident[len(Z2M_IDENTIFIER_PREFIX):]
            label = device.name_by_user or device.name or topic
            options.append(
                selector.SelectOptionDict(value=topic, label=f"{label} ({topic})")
            )
    return options


def _build_zha_options(hass: HomeAssistant) -> list[selector.SelectOptionDict]:
    """Build dropdown options for ZHA devices.

    Each option's value is the IEEE address, taken from the 'zha' device
    identifier.
    """
    dev_reg = dr.async_get(hass)
    options: list[selector.SelectOptionDict] = []
    for device in dev_reg.devices.values():
        for domain, ident in device.identifiers:
            if domain != "zha":
                continue
            label = device.name_by_user or device.name or ident
            options.append(
                selector.SelectOptionDict(value=ident, label=f"{label} ({ident})")
            )
    return options


def _build_entity_options(
    hass: HomeAssistant, domain: str
) -> list[selector.SelectOptionDict]:
    """Build dropdown options for entities in a given domain (e.g. tts, media_player)."""
    ent_reg = er.async_get(hass)
    options: list[selector.SelectOptionDict] = []
    for entity in ent_reg.entities.values():
        if entity.domain != domain:
            continue
        label = entity.name or entity.original_name or entity.entity_id
        options.append(
            selector.SelectOptionDict(value=entity.entity_id, label=f"{label} ({entity.entity_id})")
        )
    return options


def _select(options: list[selector.SelectOptionDict]) -> selector.SelectSelector:
    """A single-select dropdown that also allows free-text custom values.

    When no options are discovered the dropdown is empty but the user can
    still type a value manually (custom_value=True).
    """
    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=options,
            custom_value=True,
            mode=selector.SelectSelectorMode.DROPDOWN,
        )
    )


def _clean(value) -> str:
    """Normalize a free-text/selector value: strip surrounding whitespace."""
    if isinstance(value, str):
        return value.strip()
    return value


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
            self._data[CONF_PLATFORM] = user_input[CONF_PLATFORM]
            self._data[CONF_Z2M_TOPIC] = _clean(user_input.get(CONF_Z2M_TOPIC, ""))
            self._data[CONF_ZHA_IEEE] = _clean(user_input.get(CONF_ZHA_IEEE, ""))
            return await self.async_step_features()

        z2m_options = _build_z2m_options(self.hass)
        zha_options = _build_zha_options(self.hass)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PLATFORM, default=PLATFORM_Z2M): vol.In(
                        {PLATFORM_Z2M: "Zigbee2MQTT", PLATFORM_ZHA: "ZHA"}
                    ),
                    vol.Optional(CONF_Z2M_TOPIC, default=""): _select(z2m_options),
                    vol.Optional(CONF_ZHA_IEEE, default=""): _select(zha_options),
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
            self._data[CONF_TTS_ENGINE] = _clean(user_input.get(CONF_TTS_ENGINE, DEFAULT_TTS_ENGINE))
            self._data[CONF_TTS_SPEAKER] = _clean(user_input.get(CONF_TTS_SPEAKER, ""))
            identifier = self._data.get(CONF_Z2M_TOPIC) or self._data.get(CONF_ZHA_IEEE) or "Unknown"
            title = f"ThirdReality Scale ({identifier})"
            return self.async_create_entry(title=title, data=self._data)

        tts_options = _build_entity_options(self.hass, "tts")
        speaker_options = _build_entity_options(self.hass, "media_player")

        return self.async_show_form(
            step_id="voice",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_TTS_ENGINE, default=DEFAULT_TTS_ENGINE): _select(tts_options),
                    vol.Optional(CONF_TTS_SPEAKER, default=""): _select(speaker_options),
                }
            ),
            errors=errors,
        )
