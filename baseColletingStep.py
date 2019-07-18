# -*- coding: utf-8 -*-

from modules.core.props import Property, StepProperty
from modules import cbpi

class BaseColletingStep(object):
    collectingActor = StepProperty.Actor("Collecting actor", description="Collecting device")
    collectingSensor = StepProperty.Sensor("Collecting indicator", description="Shows the rate of selection")

    isPaused = False
    power = 0
    maxSpeed = 0

    @cbpi.action("Start collecting")
    def start(self):
        if self.isPaused:
            self.time = datetime.utcnow()
            self.notify("", "Collecting continued", type="success", timeout=2000)
            self.isPaused = False

    @cbpi.action("Stop collecting")
    def stop(self):
        if not self.isPaused:
            self.notify("", "Collecting paused", type="success", timeout=2000)
            self.isPaused = True

    def notifySensor(self):
        try:
            sensor = self.api.cache.get("sensors").get(int(self.collectingSensor)).instance
            sensor.collecting = int(self.collectingSpeed)
        except:
            pass

    def updateMaxCollectingSpeed(self):
        try:
            actor = self.api.cache.get("actors").get(int(self.collectingActor)).instance
            self.maxSpeed = actor.get_max_speed()
        except:
            self.maxSpeed = 0

    def manageActor(self):
        actorId = int(self.collectingActor)
        self.actor_power(power=self.power, id=actorId)
        if self.isPaused:
            self.actor_off(actorId)
        else:
            self.actor_on(power=self.power, id=actorId)

    def calculateActorPower(self):
        if self.maxSpeed > 0:
            self.power = min(round(float(self.collectingSpeed) / self.maxSpeed  * 100), 100)