from modules import cbpi
from modules.core.hardware import  SensorActive
from modules.core.props import Property

@cbpi.sensor
class PickingSensor(SensorActive):
    collecting = 0

    def get_unit(self):
        '''
        :return: Unit of the sensor as string. Should not be longer than 3 characters
        '''
        return "ml/h"

    def stop(self):
        '''
        Stop the sensor. Is called when the sensor config is updated or the sensor is deleted
        :return: 
        '''
        self.collecting = 0

    def execute(self):
        '''
        Active sensor has to handle its own loop
        :return: 
        '''
        while self.is_running():
            self.data_received(self.collecting)
            self.sleep(5)