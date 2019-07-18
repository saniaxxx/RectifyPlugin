# -*- coding: utf-8 -*-

from modules import cbpi
from modules.core.props import Property
from modules.base_plugins.gpio_actor import GPIOPWM

try:
    import RPi.GPIO as GPIO
except Exception as e:
    print e


@cbpi.actor
class CollectingActor(GPIOPWM):
    maxSpeed = Property.Number("Maximum collecting speed of actor, ml/h", configurable=True, default_value=1000)

    def init(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(int(self.gpio), GPIO.OUT)
        GPIO.output(int(self.gpio), 0)

    def get_max_speed(self):
        return int(self.maxSpeed)

    def on(self, power=None):
        if power is not None:
            self.power = int(power)

        if self.frequency is None:
            self.frequency = 0.5  # 2 sec

        try:
            self.p = GPIO.PWM(int(self.gpio), float(self.frequency))
        except RuntimeError as e:
            self.init()
            self.p = GPIO.PWM(int(self.gpio), float(self.frequency))
        self.p.start(int(self.power))