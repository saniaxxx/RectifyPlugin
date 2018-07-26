# -*- coding: utf-8 -*-

from modules.core.props import Property, StepProperty
from modules.core.step import StepBase
from modules import cbpi

@cbpi.step
class HeartsStep(StepBase):
    actor = StepProperty.Actor("Actor", description="Collecting device")
    kettle = StepProperty.Kettle("Kettle", description="Pot-still")

    refluxRatio = Property.Number("Reflux ratio", configurable=True,default_value=3)
    maxSpeed = Property.Number("Maximum collecting speed of actor, ml/h", configurable=True, default_value=1000)
    heaterPower = Property.Number("Heater power, watt", configurable=True, default_value=1000)
    endTemp = Property.Number("Completion temperature, degree Celsius", configurable=True, default_value=93)
    
    isPaused = False
    collecting = 0.0
    temperature = 0
    power = 0

    @cbpi.action("Start collecting")
    def start(self):
        self.notify("", "Collection of hearts continued", type="warning", timeout=2000)
        self.isPaused = False

    @cbpi.action("Stop collecting")
    def stop(self):
        self.notify("", "Collecting hearts is paused", type="warning", timeout=2000)
        self.isPaused = True

    def finish(self):
        self.actor_off(int(self.actor))
        self.notify("", "Collecting hearts completed", type="success", timeout=2000)

    def execute(self):
        self.updateAndCheckTemperature()
        self.recountCollecting()
        self.calculateActorPower()
        self.manageActor()

    def calculateActorPower(self):
        self.power = min(round(self.collecting / float(self.maxSpeed)  * 100), 100)

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
        W = float(self.heaterPower)
        R = float(self.refluxRatio)
        Q = K*(100 - T)*W/(R + 1)
        if abs(self.collecting - Q) > 0:
            self.notify("", "Now collecting speed is " + str(Q) + "ml/h", type="warning", timeout=2000)
        self.collecting = Q

    def updateAndCheckTemperature(self):
        self.temperature = self.get_kettle_temp(self.kettle)
        if self.temperature >= int(self.endTemp):
            self.next()

