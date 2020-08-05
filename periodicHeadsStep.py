# -*- coding: utf-8 -*-

from modules.core.props import Property, StepProperty
from modules.core.step import StepBase
from .baseColletingStep import BaseColletingStep
from modules import cbpi
from datetime import datetime

@cbpi.step
class PeriodicHeadsStep(StepBase, BaseColletingStep):
    closedTime = Property.Number("Время накопления, мин", configurable=True, default_value=10)
    openTime = Property.Number("Время сброса, сек", configurable=True, default_value=60)
    headsTotal = Property.Number("Объем голов для отбора, мл", configurable=True, default_value=100)

    collectingSpeed = 0
    total = 0
    time = datetime.utcnow()
    timePeriod = datetime.utcnow()
    collecting = True

    def init(self):
        self.reset()

    def reset(self):
        self.time = datetime.utcnow()
        self.timePeriod = datetime.utcnow()
        self.total = 0
        self.power = 100
        self.collecting = True

    def finish(self):
        self.actor_off(int(self.collectingActor))
        self.notify("", "Отбор голов завершен", type="success", timeout=2000)

    def execute(self):
        self.setCollectingSpeed()
        self.updateMaxCollectingSpeed()
        self.calculateActorPower()
        self.manageActor()
        self.checkTotalCollecting()
        self.notifySensor()

    def setCollectingSpeed(self):
        self.collectingSpeed = self.maxSpeed

    def calculateActorPower(self):
        timePeriod = datetime.utcnow()
        if self.collecting and float((timePeriod-self.timePeriod).total_seconds()) > float(self.openTime):
            self.collecting = False
            self.timePeriod = timePeriod
            self.power = 0
        elif not self.collecting and float((timePeriod-self.timePeriod).total_seconds()) > float(self.closedTime) * 60:
            self.collecting = True
            self.timePeriod = timePeriod
            self.power = 100

    def checkTotalCollecting(self):
        time = datetime.utcnow()
        if (time-self.time).total_seconds() >= 1:
            self.time = time
            if self.collecting:
                self.total += float(self.collectingSpeed)/3600.0

        if self.total >= int(self.headsTotal):
            self.isPaused = True
