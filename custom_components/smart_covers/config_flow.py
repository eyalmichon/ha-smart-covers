from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
import voluptuous as vol

from .const import DOMAIN


class SmartCoversConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the initial configuration (async_step_user)."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @callback
    def _get_entity_ids(self):
        return self.hass.states.async_entity_ids()

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input["ent_name"],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("ent_name"): str,
                    vol.Required("entity_up"): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=["switch"],
                            multiple=False,
                        )
                    ),
                    vol.Required("entity_down"): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=["switch"],
                            multiple=False,
                        )
                    ),
                    vol.Required("time_up", default=0.0): vol.All(
                        vol.Coerce(float), vol.Range(min=0)
                    ),
                    vol.Required("time_down", default=0.0): vol.All(
                        vol.Coerce(float), vol.Range(min=0)
                    ),
                    vol.Required("tilt_open", default=0.0): vol.All(
                        vol.Coerce(float), vol.Range(min=0)
                    ),
                    vol.Required("tilt_closed", default=0.0): vol.All(
                        vol.Coerce(float), vol.Range(min=0)
                    ),

                    vol.Required("timed_control_down", default=False): bool,
                    vol.Optional("time_to_roll_down", default="12:00"): vol.All(
                        vol.Coerce(str)
                    ),
                    vol.Required("timed_control_up", default=False): bool,
                    vol.Optional("time_to_roll_up", default="12:00"): vol.All(
                        vol.Coerce(str)
                    ),

                    vol.Required("delay_control", default=False): bool,
                    vol.Optional("delay_sunrise", default=0): vol.All(vol.Coerce(int)),
                    vol.Optional("delay_sunset", default=0): vol.All(vol.Coerce(int)),

                    vol.Required("night_lights", default=False): bool,
                    vol.Optional("entity_night_lights"): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=["light", "switch"],
                            multiple=False,
                        )
                    ),

                    vol.Required("tilting_day", default=False): bool,

                    vol.Required("protect_the_cover", default=False): bool,
                    vol.Optional("wind_speed", default=30): vol.All(vol.Coerce(float)),
                    vol.Optional("wmo_code", default=80): vol.All(vol.Coerce(int)),

                    vol.Required("netamo_enable", default=False): bool,
                    vol.Optional("netamo_speed_entity"): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=["sensor"],
                            device_class=["wind_speed"],
                            multiple=False,
                        )
                    ),
                    vol.Optional("netamo_speed", default=30): vol.All(vol.Coerce(float)),
                    vol.Optional("netamo_gust_entity"): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=["sensor"],
                            device_class=["wind_speed"],
                            multiple=False,
                        )
                    ),
                    vol.Optional("netamo_gust", default=40): vol.All(vol.Coerce(float)),
                    vol.Optional("netamo_rain_entity"): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=["sensor"],
                            device_class=["precipitation"],
                            multiple=False,
                        )
                    ),
                    vol.Optional("netamo_rain", default=40): vol.All(vol.Coerce(float)),

                    vol.Required("send_stop_at_end", default=True): bool,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SmartCoversOptionsFlow(config_entry)


class SmartCoversOptionsFlow(config_entries.OptionsFlow):
    """Handle updates to an existing entry (async_step_init)."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    @callback
    def _get_entity_ids(self):
        return self.hass.states.async_entity_ids()

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            # Merge whatever the user changed over the existing data
            updated_data = {**self.config_entry.data, **user_input}
            self.hass.config_entries.async_update_entry(
                entry=self.config_entry, data=updated_data
            )
            # Reload the integration to apply the new configuration
            await self.hass.config_entries.async_reload(self.config_entry.entry_id)
            return self.async_create_entry(title="", data={})

        data_schema_dict = {}

        # 1) ent_name
        data_schema_dict[
            vol.Required(
                "ent_name",
                default=self.config_entry.data.get("ent_name", ""),
            )
        ] = str

        # 2) entity_up
        data_schema_dict[
            vol.Required(
                "entity_up",
                default=self.config_entry.data["entity_up"],
            )
        ] = selector.EntitySelector(
            selector.EntitySelectorConfig(
                domain=["switch", "input_boolean", "binary_sensor"],
                multiple=False,
            )
        )

        # 3) entity_down
        data_schema_dict[
            vol.Required(
                "entity_down",
                default=self.config_entry.data["entity_down"],
            )
        ] = selector.EntitySelector(
            selector.EntitySelectorConfig(
                domain=["switch", "input_boolean", "binary_sensor"],
                multiple=False,
            )
        )

        # 4) time_up, time_down, tilt_open, tilt_closed
        data_schema_dict[
            vol.Required(
                "time_up",
                default=self.config_entry.data.get("time_up", 0.0),
            )
        ] = vol.All(vol.Coerce(float), vol.Range(min=0))
        data_schema_dict[
            vol.Required(
                "time_down",
                default=self.config_entry.data.get("time_down", 0.0),
            )
        ] = vol.All(vol.Coerce(float), vol.Range(min=0))
        data_schema_dict[
            vol.Required(
                "tilt_open",
                default=self.config_entry.data.get("tilt_open", 0.0),
            )
        ] = vol.All(vol.Coerce(float), vol.Range(min=0))
        data_schema_dict[
            vol.Required(
                "tilt_closed",
                default=self.config_entry.data.get("tilt_closed", 0.0),
            )
        ] = vol.All(vol.Coerce(float), vol.Range(min=0))

        # 5) timed_control_down / time_to_roll_down / timed_control_up / time_to_roll_up
        data_schema_dict[
            vol.Required(
                "timed_control_down",
                default=self.config_entry.data.get("timed_control_down", False),
            )
        ] = bool
        data_schema_dict[
            vol.Optional(
                "time_to_roll_down",
                default=self.config_entry.data.get("time_to_roll_down", "12:00"),
            )
        ] = vol.All(vol.Coerce(str))
        data_schema_dict[
            vol.Required(
                "timed_control_up",
                default=self.config_entry.data.get("timed_control_up", False),
            )
        ] = bool
        data_schema_dict[
            vol.Optional(
                "time_to_roll_up",
                default=self.config_entry.data.get("time_to_roll_up", "12:00"),
            )
        ] = vol.All(vol.Coerce(str))

        # 6) delay_control / delay_sunrise / delay_sunset
        data_schema_dict[
            vol.Required(
                "delay_control",
                default=self.config_entry.data.get("delay_control", False),
            )
        ] = bool
        data_schema_dict[
            vol.Optional(
                "delay_sunrise",
                default=self.config_entry.data.get("delay_sunrise", 0),
            )
        ] = vol.All(vol.Coerce(int))
        data_schema_dict[
            vol.Optional(
                "delay_sunset",
                default=self.config_entry.data.get("delay_sunset", 0),
            )
        ] = vol.All(vol.Coerce(int))

        # 7) night_lights + optional entity_night_lights
        data_schema_dict[
            vol.Required(
                "night_lights",
                default=self.config_entry.data.get("night_lights", False),
            )
        ] = bool

        existing_night = self.config_entry.data.get("entity_night_lights")
        if existing_night:
            data_schema_dict[
                vol.Optional("entity_night_lights", default=existing_night)
            ] = selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["light", "switch", "input_boolean"],
                    multiple=False,
                )
            )
        else:
            data_schema_dict[
                vol.Optional("entity_night_lights")
            ] = selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["light", "switch", "input_boolean"],
                    multiple=False,
                )
            )

        # 8) tilting_day
        data_schema_dict[
            vol.Required(
                "tilting_day",
                default=self.config_entry.data.get("tilting_day", False),
            )
        ] = bool

        # 9) protect_the_cover / wind_speed / wmo_code
        data_schema_dict[
            vol.Required(
                "protect_the_cover",
                default=self.config_entry.data.get("protect_the_cover", False),
            )
        ] = bool
        data_schema_dict[
            vol.Optional(
                "wind_speed",
                default=self.config_entry.data.get("wind_speed", 30),
            )
        ] = vol.All(vol.Coerce(float))
        data_schema_dict[
            vol.Optional(
                "wmo_code",
                default=self.config_entry.data.get("wmo_code", 80),
            )
        ] = vol.All(vol.Coerce(int))

        # 10) netamo_enable / netamo_*_entity / netamo_* values
        data_schema_dict[
            vol.Required(
                "netamo_enable",
                default=self.config_entry.data.get("netamo_enable", False),
            )
        ] = bool

        existing_speed_ent = self.config_entry.data.get("netamo_speed_entity")
        if existing_speed_ent:
            data_schema_dict[
                vol.Optional("netamo_speed_entity", default=existing_speed_ent)
            ] = selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["sensor"],
                    device_class=["wind_speed"],
                    multiple=False,
                )
            )
        else:
            data_schema_dict[
                vol.Optional("netamo_speed_entity")
            ] = selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["sensor"],
                    device_class=["wind_speed"],
                    multiple=False,
                )
            )

        data_schema_dict[
            vol.Optional(
                "netamo_speed",
                default=self.config_entry.data.get("netamo_speed", 30),
            )
        ] = vol.All(vol.Coerce(float))

        existing_gust_ent = self.config_entry.data.get("netamo_gust_entity")
        if existing_gust_ent:
            data_schema_dict[
                vol.Optional("netamo_gust_entity", default=existing_gust_ent)
            ] = selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["sensor"],
                    device_class=["wind_speed"],
                    multiple=False,
                )
            )
        else:
            data_schema_dict[
                vol.Optional("netamo_gust_entity")
            ] = selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["sensor"],
                    device_class=["wind_speed"],
                    multiple=False,
                )
            )

        data_schema_dict[
            vol.Optional(
                "netamo_gust",
                default=self.config_entry.data.get("netamo_gust", 40),
            )
        ] = vol.All(vol.Coerce(float))

        existing_rain_ent = self.config_entry.data.get("netamo_rain_entity")
        if existing_rain_ent:
            data_schema_dict[
                vol.Optional("netamo_rain_entity", default=existing_rain_ent)
            ] = selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["sensor"],
                    device_class=["precipitation"],
                    multiple=False,
                )
            )
        else:
            data_schema_dict[
                vol.Optional("netamo_rain_entity")
            ] = selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["sensor"],
                    device_class=["precipitation"],
                    multiple=False,
                )
            )

        data_schema_dict[
            vol.Optional(
                "netamo_rain",
                default=self.config_entry.data.get("netamo_rain", 40),
            )
        ] = vol.All(vol.Coerce(float))

        # 11) send_stop_at_end
        data_schema_dict[
            vol.Required(
                "send_stop_at_end",
                default=self.config_entry.data.get("send_stop_at_end", True),
            )
        ] = bool

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(data_schema_dict),
        )
