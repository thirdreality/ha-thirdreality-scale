"""Scale hardware commands for ThirdReality Smart Scale.

Encapsulates Z2M (MQTT) and ZHA commands for:
- tare (zero/reset)
- start_report (begin weight reporting)
- stop_report (stop weight reporting)
- set_weight (set target weight for auto-advance)
"""
from __future__ import annotations

import logging
from homeassistant.core import HomeAssistant

from .const import PLATFORM_Z2M

_LOGGER = logging.getLogger(__name__)


class ScaleCommands:
    """Send hardware commands to the scale via Z2M or ZHA."""

    def __init__(
        self, hass: HomeAssistant, platform: str, z2m_topic: str, zha_ieee: str
    ) -> None:
        """Initialize."""
        self._hass = hass
        self._platform = platform
        self._z2m_topic = z2m_topic
        self._zha_ieee = zha_ieee

    async def tare(self) -> None:
        """Zero/reset the scale."""
        if self._platform == PLATFORM_Z2M:
            await self._mqtt_publish({"reset_button": "RESET"})
        else:
            await self._zha_command(command=0)

    async def start_report(self) -> None:
        """Start continuous weight reporting."""
        if self._platform == PLATFORM_Z2M:
            await self._mqtt_publish({"start_report_button": "START"})
        else:
            await self._zha_command(command=1)

    async def stop_report(self) -> None:
        """Stop continuous weight reporting."""
        if self._platform == PLATFORM_Z2M:
            await self._mqtt_publish({"stop_report_button": "STOP"})
        else:
            await self._zha_command(command=2)

    async def set_weight(self, weight: int) -> None:
        """Set target weight (grams) for auto-advance notification."""
        if self._platform == PLATFORM_Z2M:
            await self._mqtt_publish({"set_weight_button": str(weight)})
        else:
            await self._zha_command(command=3, params={"target_val": weight})

    async def _mqtt_publish(self, payload: dict) -> None:
        """Publish a command to Z2M via MQTT."""
        import json

        topic = f"zigbee2mqtt/{self._z2m_topic}/set"
        try:
            await self._hass.services.async_call(
                "mqtt",
                "publish",
                {"topic": topic, "payload": json.dumps(payload)},
                blocking=True,
            )
        except Exception as err:
            _LOGGER.warning("MQTT publish failed: %s", err)

    async def _zha_command(self, command: int, params: dict | None = None) -> None:
        """Send a ZHA cluster command."""
        try:
            await self._hass.services.async_call(
                "zha",
                "issue_zigbee_cluster_command",
                {
                    "ieee": self._zha_ieee,
                    "endpoint_id": 1,
                    "cluster_id": 0xFF0C,
                    "cluster_type": "in",
                    "command": command,
                    "command_type": "server",
                    "manufacturer": 0x1407,
                    "params": params or {},
                },
                blocking=True,
            )
        except Exception as err:
            _LOGGER.warning("ZHA command %d failed: %s", command, err)
