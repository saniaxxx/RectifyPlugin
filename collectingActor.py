# -*- coding: utf-8 -*-

from modules import cbpi
from modules.core.props import Property
from modules.core.hardware import ActorBase
from threading import Timer

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except Exception as e:
    print e
    pass

@cbpi.actor
class CollectingActor(ActorBase):
    gpio = Property.Select("GPIO", options=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27], description="Номер GPIO порта")
    period = Property.Number("Период ШИМ (сек)", configurable=True, default_value=8)
    maxSpeed = Property.Number("Скорость отбора при 100% ШИМ, мл/ч", configurable=True, default_value=2000)
    power = 100
    enabled = False

    def init(self):
        GPIO.setup(int(self.gpio), GPIO.OUT)
        GPIO.output(int(self.gpio), 0)

    def create_timer(self):
        timeOn = self.power / 100.0 * float(self.period)
        timeOff = float(self.period) - timeOn
        if timeOff == 0:
            self.timer = Timer(float(self.period), self.switch)
        elif self.enabled:
            self.timer = Timer(timeOn, self.switch)
        else:
            self.timer = Timer(timeOff, self.switch)
        self.timer.start()

    def switch(self):
        if hasattr(self, "timer") and self.timer is not None:
            self.timer.cancel()
            self.timer = None
        if self.enabled and self.power < 100:
            self.disable()
            self.enabled = False
        else:
            self.enable()
            self.enabled = True
        self.create_timer()

    def on(self, power=0):
        self.set_power(power)
        self.switch()

    def off(self):
        self.timer.cancel()
        self.timer = None
        self.disable()
        self.enabled = False

    def set_power(self, power):
        if power is not None:
            self.power = int(power)

    def stop(self):
        self.timer.cancel()
        self.timer = None

    def enable(self):
        print "GPIO ON %s" % str(self.gpio)
        GPIO.output(int(self.gpio), 1)

    def disable(self):
        print "GPIO OFF"
        GPIO.output(int(self.gpio), 0)

    def get_max_speed(self):
        return int(self.maxSpeed)