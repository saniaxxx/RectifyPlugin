# -*- coding: utf-8 -*-

from modules.core.props import Property, StepProperty
from modules.core.step import StepBase
from modules import cbpi
from datetime import datetime
from rectifyConfig import RectifyConfig

@cbpi.step
class HeadsStep(StepBase):
    actor = StepProperty.Actor("Actor", description="Collecting device")
    collectingSpeed = Property.Number("Heads collecting speed, ml/h", configurable=True, default_value=100)
    headsTotal = Property.Number("Heads total, ml", configurable=True, default_value=100)
    
    isPaused = False
    collecting = 0.0
    total = 0
    power = 0
    time = datetime.utcnow()

    @cbpi.action("Start collecting")
    def start(self):
        if self.isPaused:
            self.time = datetime.utcnow()
            self.notify("", "Collection of collectingSpeed continued", type="success", timeout=2000)
            self.isPaused = False

    @cbpi.action("Stop collecting")
    def stop(self):
        if not self.isPaused:
            self.notify("", "Collecting heads is paused", type="success", timeout=2000)
            self.isPaused = True

    def finish(self):
        self.actor_off(int(self.actor))
        self.notify("", "Collecting heads completed", type="success", timeout=2000)

    def execute(self):
        self.manageActor()
        self.checkTotalCollecting()

    def init(self):
        self.power = min(round(float(self.collectingSpeed) / float(RectifyConfig.maxSpeed())  * 100), 100)

    def manageActor(self):
        actorId = int(self.actor)
        self.actor_power(power=self.power, id=actorId)
        if self.isPaused:
            self.actor_off(self.actorId())
        else:
            self.actor_on(power=self.power, id=actorId)

    def checkTotalCollecting(self):
        time = datetime.utcnow()
        if (time-self.time).total_seconds() > 10:
            self.time = time
            self.total += float(self.collectingSpeed)/360.0
            self.notify("", "Collected: " + "%.1f" % self.total + " ml", type="success", timeout=2000)

        if self.total >= int(self.headsTotal):
            self.next()
