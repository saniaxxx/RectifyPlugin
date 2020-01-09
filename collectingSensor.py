# -*- coding: utf-8 -*-

from modules import cbpi
from modules.core.hardware import  SensorActive
from modules.core.props import Property

@cbpi.sensor
class CollectingSensor(SensorActive):
    collecting = 0

    def get_unit(self):
        '''
        :return: Unit of the sensor as string. Should not be longer than 3 characters
        '''
        return "мл/ч"

    def execute(self):
        '''
        Active sensor has to handle its own loop
        :return: 
        '''
        while self.is_running():
            self.data_received(self.collecting)
            self.sleep(5)