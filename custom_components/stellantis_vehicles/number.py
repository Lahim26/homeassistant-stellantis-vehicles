import logging

from homeassistant.const import PERCENTAGE
from homeassistant.components.number import NumberEntityDescription
from homeassistant.components.number.const import NumberMode
from .base import StellantisBaseNumberSensor

from .const import (
    DOMAIN
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities) -> None:
    stellantis = hass.data[DOMAIN][entry.entry_id]
    entities = []

    vehicles = await stellantis.get_user_vehicles()

    for vehicle in vehicles:
        coordinator = await stellantis.async_get_coordinator(vehicle)
        if coordinator._data["service"]["type"] == "Electric":
            description = NumberEntityDescription(
                name = "battery_charging_limit",
                key = "battery_charging_limit",
                translation_key = "battery_charging_limit",
                icon = "mdi:battery-charging-60",
                unit_of_measurement = PERCENTAGE,
                min_value = 20,
                max_value = 90,
                step = 1,
                mode = NumberMode.SLIDER
            )
            entities.extend([StellantisBaseNumberSensor(coordinator, description)])

    async_add_entities(entities)