# -*- coding: utf-8 -*-

from modules.core.props import Property, StepProperty
from modules.core.step import StepBase
from baseColletingStep import BaseColletingStep
from modules import cbpi

@cbpi.step
class HeartsStep(StepBase, BaseColletingStep):
    temperatureSensor = StepProperty.Sensor("Temperature sensor", description="Temperature sensor inside pot-still")
    initialCollecting = Property.Number("Initial collecting, ml/h", configurable=True, default_value=1000)
    endTemp = Property.Number("Completion temperature, degree Celsius", configurable=True, default_value=93)
    
    collectingSpeed = 0.0
    temperature = 0

    def finish(self):
        self.actor_off(int(self.collectingActor))
        self.notify("", "Collecting hearts completed", type="success", timeout=2000)

    def execute(self):
        self.updateAndCheckTemperature()
        self.recountCollecting()
        self.notifySensor()
        self.updateMaxCollectingSpeed()
        self.calculateActorPower()
        self.manageActor()

    def recountCollecting(self):
        a = - 76.923
        b = 7538.561
        k = (a * self.temperature + b) / 1000
        k = min(k, 1)
        self.collectingSpeed = int(self.initialCollecting * k)

    def updateAndCheckTemperature(self):
        self.temperature = float(self.get_sensor_value(int(self.temperatureSensor)))
        if self.temperature >= int(self.endTemp):
            self.next()