# -*- coding: utf-8 -*-

from modules import cbpi
from modules.core.props import Property
from modules.base_plugins.gpio_actor import GPIOPWM

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except Exception as e:
    print e


@cbpi.actor
class CollectingActor(GPIOPWM):
    maxSpeed = Property.Number("Maximum collecting speed of actor, ml/h", configurable=True, default_value=1000)

    def get_max_speed(self):
        return int(self.maxSpeed)