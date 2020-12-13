# -*- coding: utf-8 -*-

from modules.core.props import Property, StepProperty
from modules.core.step import StepBase
from .baseColletingStep import BaseColletingStep
from modules import cbpi

@cbpi.step
class StartStopStep(StepBase, BaseColletingStep):
    temperatureSensor = StepProperty.Sensor("Датчик температуры", description="Датчик температуры в царге")
    initialCollecting = Property.Number("Стартовая скорость отбора, мл/ч", configurable=True, default_value=1000)
    deltaTemp = Property.Number("Разрешенный залет температуры, °C", configurable=True, default_value=0.3)
    decrement = Property.Number("Уменьшение отбора при залете температуры, %", configurable=True, default_value=10)
    endTemp = Property.Number("Температура завершения отбора", configurable=True, default_value=93)
    
    initialTemp = None
    currentCollecting = None
    collectingSpeed = 0.0
    temperature = 0
    stopped = False

    def finish(self):
        self.actor_off(int(self.collectingActor))
        self.notify("", "Отбор тела завершен", type="success", timeout=2000)

    def execute(self):
        self.updateAndCheckTemperature()
        self.recountCollecting()
        self.notifySensor()
        self.updateMaxCollectingSpeed()
        self.calculateActorPower()
        self.manageActor()

    def recountCollecting(self):
        if not self.currentCollecting:
            self.currentCollecting = int(self.initialCollecting)
        if not self.initialTemp:
            self.initialTemp = float(self.temperature)
        if self.stopped:
            self.stopped = float(self.temperature) > self.initialTemp
        elif self.temperature and float(self.temperature) - self.initialTemp > float(self.deltaTemp):
            self.stopped = True
            self.currentCollecting = self.currentCollecting * (100 - int(self.decrement)) / 100
        self.collectingSpeed = 0 if self.stopped else self.currentCollecting

    def updateAndCheckTemperature(self):
        self.temperature = float(self.get_sensor_value(int(self.temperatureSensor)))
        if self.temperature >= int(self.endTemp):
            next(self)
