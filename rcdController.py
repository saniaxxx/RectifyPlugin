# -*- coding: utf-8 -*-

from modules import cbpi
from modules.core.controller import KettleController

@cbpi.controller
class RCDController(KettleController):
    def run(self):
        while self.is_running():
            if self.get_temp() >= self.get_target_temp():
                self.heater_on(100)
            else:
                self.heater_off()
            self.sleep(1)
