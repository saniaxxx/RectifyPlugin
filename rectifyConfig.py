from modules import cbpi

class RectifyConfig(object):
    REFLUX_RATIO_KEY = "reflux_ratio"
    MAX_COLLECTING_SPEED_KEY = "max_collecting_speed"
    HEATER_POWER_KEY = "heater_power"

    REFLUX_RATIO_DEFAULT = 3
    MAX_COLLECTING_SPEED_DEFAULT = 1000
    HEATER_POWER_DEFAULT = 1000

    @classmethod
    def configure(self):
        cbpi.app.logger.info("### CONFIGURE RectifyPlugin ###")
        self.setupNumberParameter(RectifyConfig.REFLUX_RATIO_KEY, RectifyConfig.REFLUX_RATIO_DEFAULT, "Reflux ratio")
        self.setupNumberParameter(RectifyConfig.MAX_COLLECTING_SPEED_KEY, RectifyConfig.MAX_COLLECTING_SPEED_DEFAULT, "Maximum collecting speed of actor, ml/h")
        self.setupNumberParameter(RectifyConfig.HEATER_POWER_KEY, RectifyConfig.HEATER_POWER_DEFAULT, "Heater power, watt")

    @classmethod
    def setupNumberParameter(self, name, default_value, description):
        value = cbpi.get_config_parameter(name, None)
        if value is None:
            cbpi.add_config_parameter(name, default_value, "number", description)

    @classmethod
    def refluxRatio(self):
        return cbpi.get_config_parameter(RectifyConfig.REFLUX_RATIO_KEY, RectifyConfig.REFLUX_RATIO_DEFAULT)

    @classmethod
    def maxSpeed(self):
        return cbpi.get_config_parameter(RectifyConfig.MAX_COLLECTING_SPEED_KEY, RectifyConfig.MAX_COLLECTING_SPEED_DEFAULT)

    @classmethod
    def heaterPower(self):
        return cbpi.get_config_parameter(RectifyConfig.HEATER_POWER_KEY, RectifyConfig.HEATER_POWER_DEFAULT)


@cbpi.initalizer()
def init(cbpi):
    RectifyConfig.configure()