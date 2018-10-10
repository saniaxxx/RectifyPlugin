# -*- coding: utf-8 -*-

from modules import cbpi
from modules.core.hardware import  SensorActive
from modules.core.props import Property

@cbpi.sensor
class PowerSensor(SensorActive):
    power = Property.Number("heater power, Watt", configurable=True, default_value=1000)

    def get_unit(self):
        '''
        :return: Unit of the sensor as string. Should not be longer than 3 characters
        '''
        return "Watt"

    def execute(self):
        '''
        Active sensor has to handle its own loop
        :return: 
        '''
        while self.is_running():
            self.data_received(int(self.power))
            self.sleep(5)