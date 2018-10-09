# -*- coding: utf-8 -*-

from modules.core.props import Property, StepProperty
from modules.core.step import StepBase
from modules import cbpi
from rectifyConfig import RectifyConfig

@cbpi.step
class HeartsStep(StepBase):
    temperatureSensor = StepProperty.Sensor("Temperature sensor", description="Temperature sensor inside pot-still")
    collectingSensor = StepProperty.Sensor("Collecting indicator", description="Collecting indicator")
    actor = StepProperty.Actor("Actor", description="Collecting device")
    endTemp = Property.Number("Completion temperature, degree Celsius", configurable=True, default_value=93)
    
    isPaused = False
    collecting = 0.0
    temperature = 0
    power = 0

    @cbpi.action("Start collecting")
    def start(self):
        if self.isPaused:
            self.notify("", "Collection of hearts continued", type="success", timeout=2000)
            self.isPaused = False

    @cbpi.action("Stop collecting")
    def stop(self):
        if not self.isPaused:
            self.notify("", "Collecting hearts is paused", type="success", timeout=2000)
            self.isPaused = True

    def finish(self):
        self.actor_off(int(self.actor))
        self.notify("", "Collecting hearts completed", type="success", timeout=2000)

    def execute(self):
        self.updateAndCheckTemperature()
        self.recountCollecting()
        self.notifySensor()
        self.calculateActorPower()
        self.manageActor()

    def calculateActorPower(self):
        self.power = min(round(self.collecting / float(RectifyConfig.maxSpeed())  * 100), 100)

    def manageActor(self):
        actorId = int(self.actor)
        self.actor_power(power=self.power, id=actorId)
        if self.isPaused:
            self.actor_off(self.actorId())
        else:
            self.actor_on(power=self.power, id=actorId)

    def recountCollecting(self):
        K = 0.174
        T = float(self.temperature)
        W = float(RectifyConfig.heaterPower())
        R = float(RectifyConfig.refluxRatio())
        self.collecting = K*(100 - T)*W/(R + 1)

    def notifySensor(self):
        sensor = self.api.cache.get("sensors").get(int(self.collectingSensor)).instance
        if hasattr(sensor, 'collecting'):
            sensor.collecting = self.collecting

    def updateAndCheckTemperature(self):
        self.temperature = self.get_sensor_value(int(self.temperatureSensor))
        if self.temperature >= int(self.endTemp):
            self.next()

