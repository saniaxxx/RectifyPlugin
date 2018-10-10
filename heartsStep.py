# -*- coding: utf-8 -*-

from modules.core.props import Property, StepProperty
from modules.core.step import StepBase
from rectifyBaseStep import RectifyBaseStep
from modules import cbpi

@cbpi.step
class HeartsStep(StepBase, RectifyBaseStep):
    temperatureSensor = StepProperty.Sensor("Temperature sensor", description="Temperature sensor inside pot-still")
    powerSensor = StepProperty.Sensor("Heater power sensor", description="Required for picking speed calculation")
    endTemp = Property.Number("Completion temperature, degree Celsius", configurable=True, default_value=93)
    refluxRatio = Property.Number("Reflux ratio", configurable=True, default_value=3)
    
    collectingSpeed = 0.0
    temperature = 0
    heaterPower = 0

    def finish(self):
        self.actor_off(int(self.pickingActor))
        self.notify("", "Collecting hearts completed", type="success", timeout=2000)

    def execute(self):
        self.updateAndCheckTemperature()
        self.updateHeaterPower()
        self.recountCollecting()
        self.notifySensor()
        self.updateMaxCollectingSpeed()
        self.calculateActorPower()
        self.manageActor()

    def updateHeaterPower(self):
        try:
            sensor = self.api.cache.get("sensors").get(int(self.powerSensor)).instance
            self.heaterPower = int(sensor.power)
        except:
            pass

    def recountCollecting(self):
        K = 0.174
        T = float(self.temperature)
        W = float(self.heaterPower)
        R = float(self.refluxRatio)
        self.collectingSpeed = K*(100 - T)*W/(R + 1)

    def updateAndCheckTemperature(self):
        self.temperature = self.get_sensor_value(int(self.temperatureSensor))
        if self.temperature >= int(self.endTemp):
            self.next()