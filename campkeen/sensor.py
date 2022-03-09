"""Support for reading data from a serial port."""
from __future__ import annotations

import asyncio
import json
import logging

from serial import SerialException
import serial_asyncio
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_NAME, CONF_VALUE_TEMPLATE, EVENT_HOMEASSISTANT_STOP
from homeassistant.core import HomeAssistant, callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

CONF_SERIAL_PORT = "serial_port"
CONF_BAUDRATE = "baudrate"

DEFAULT_NAME = "CampKeen"
DEFAULT_BAUDRATE = 9600

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_SERIAL_PORT): cv.string,
        vol.Optional(CONF_BAUDRATE, default=DEFAULT_BAUDRATE): cv.positive_int,
    }
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Serial sensor platform."""
    name = config.get(CONF_NAME)
    port = config.get(CONF_SERIAL_PORT)
    baudrate = config.get(CONF_BAUDRATE)

    sensor = SerialSensor(
        name,
        port,
        baudrate
    )

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, sensor.stop_serial_read)
    async_add_entities([sensor], True)


class SerialSensor(SensorEntity):
    """Representation of a Serial sensor."""

    def __init__(
        self,
        name,
        port,
        baudrate
    ):
        """Initialize the Serial sensor."""
        self._name = name
        self._state = None
        self._port = port
        self._baudrate = baudrate
        self._bytesize = serial_asyncio.serial.EIGHTBITS
        self._parity = serial_asyncio.serial.PARITY_NONE
        self._stopbits = serial_asyncio.serial.STOPBITS_ONE
        self._xonxoff = False
        self._rtscts = False
        self._dsrdtr = False
        self._serial_loop_task = None
        self._attributes = None

    async def async_added_to_hass(self):
        """Handle when an entity is about to be added to Home Assistant."""
        self._serial_loop_task = self.hass.loop.create_task(
            self.serial_read(
                self._port,
                self._baudrate,
                self._bytesize,
                self._parity,
                self._stopbits,
                self._xonxoff,
                self._rtscts,
                self._dsrdtr,
            )
        )

    async def serial_read(
        self,
        device,
        baudrate,
        bytesize,
        parity,
        stopbits,
        xonxoff,
        rtscts,
        dsrdtr,
        **kwargs,
    ):
        """Read the data from the port."""
        logged_error = False
        while True:
            try:
                reader, _ = await serial_asyncio.open_serial_connection(
                    url=device,
                    baudrate=baudrate,
                    bytesize=bytesize,
                    parity=parity,
                    stopbits=stopbits,
                    xonxoff=xonxoff,
                    rtscts=rtscts,
                    dsrdtr=dsrdtr,
                    **kwargs,
                )

            except SerialException as exc:
                if not logged_error:
                    _LOGGER.exception(
                        "Unable to connect to the serial device %s: %s. Will retry",
                        device,
                        exc,
                    )
                    logged_error = True
                await self._handle_error()
            else:
                _LOGGER.info("Serial device %s connected", device)
                while True:
                    try:
                        line = await reader.readline()
                    except SerialException as exc:
                        _LOGGER.exception(
                            "Error while reading serial device %s: %s", device, exc
                        )
                        await self._handle_error()
                        break
                    else:
                        line = line.decode("utf-8").strip()

                        try:
                            data = json.loads(line)
                        except ValueError:
                            pass
                        else:
                            if isinstance(data, dict):
                                self._attributes = data

                        if self._template is not None:
                            line = self._template.async_render_with_possible_json_value(
                                line
                            )

                        _LOGGER.debug("Received: %s", line)
                        self._state = line
                        self.async_write_ha_state()

    async def _handle_error(self):
        """Handle error for serial connection."""
        self._state = None
        self._attributes = None
        self.async_write_ha_state()
        await asyncio.sleep(5)

    @callback
    def stop_serial_read(self, event):
        """Close resources."""
        if self._serial_loop_task:
            self._serial_loop_task.cancel()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def extra_state_attributes(self):
        """Return the attributes of the entity (if any JSON present)."""
        return self._attributes

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._state
