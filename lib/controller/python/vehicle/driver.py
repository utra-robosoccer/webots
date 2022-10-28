# Copyright 1996-2022 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from controller import Supervisor
import ctypes
import os


class Driver(Supervisor):
    INDICATOR_OFF = 0
    INDICATOR_RIGHT = 1
    INDICATOR_LEFT = 2

    def __init__(self):
        super().__init__()
        ctypes.cdll.LoadLibrary(os.path.join(os.environ['WEBOTS_HOME'], 'lib', 'controller', 'car.dll'))
        self.api = ctypes.cdll.LoadLibrary(os.path.join(os.environ['WEBOTS_HOME'], 'lib', 'controller', 'driver.dll'))
        self.api.wbu_driver_get_brake_intensity.restype = ctypes.c_double
        self.api.wbu_driver_get_steering_angle.restype = ctypes.c_double
        self.api.wbu_driver_get_target_cruising_speed.restype = ctypes.c_double
        self.api.wbu_driver_get_throttle.restype = ctypes.c_double
        self.api.wbu_driver_init()

    def __del__(self):
        self.api.wbu_driver_cleanup()

    def getBrakeIntensity(self) -> float:
        return self.brake_intensity

    def getCurrentSpeed(self) -> float:
        return self.current_speed

    def getHazardFlashers(self) -> bool:
        return self.hazard_flashers

    def getIndicator(self) -> int:
        return self.indicator

    def getSteeringAngle(self) -> float:
        return self.steering_angle

    def getTargetCruisingSpeed(self) -> float:
        return self.target_cruising_speed

    def getThrottle(self) -> float:
        return self.throttle

    def setBrakeIntensity(self, brakeIntensity: float):
        self.brake_intensity = brakeIntensity

    def setCruisingSpeed(self, cruisingSpeed: float):
        self.target_cruising_speed = cruisingSpeed

    def setHazardFlashers(self, hazardFlasher: bool):
        self.hazard_flashers = hazardFlasher

    def setIndicator(self, indicator: int):
        self.indicator = indicator

    def setSteeringAngle(self, steeringAngle: float):
        self.steering_angle = steeringAngle

    def setThrottle(self, throttle: float):
        self.throttle = throttle

    def step(self):
        return self.api.wbu_driver_step()

    @property
    def brake_intensity(self) -> float:
        return self.api.wbu_driver_get_brake_intensity()

    @brake_intensity.setter
    def brake_intensity(self, brake_intensity: float):
        self.api.wbu_driver_set_brake_intensity(ctypes.c_double(brake_intensity))

    @property
    def hazard_flashers(self) -> bool:
        return self.api.wbu_driver_get_hazard_flashers() != 0

    @hazard_flashers.setter
    def hazard_flashers(self, hazard_flashers: bool):
        self.api.wbu_driver_set_hazard_flashers(1 if hazard_flashers else 0)

    @property
    def indicator(self) -> int:
        return self.api.wbu_driver_get_indicator()

    @indicator.setter
    def indicator(self, indicator: int):
        self.api.wb_driver_set_indicator(indicator)

    @property
    def steering_angle(self) -> float:
        return self.api.wbu_driver_get_steering_angle()

    @steering_angle.setter
    def steering_angle(self, value: float):
        self.api.wbu_driver_set_steering_angle(ctypes.c_double(value))

    @property
    def current_speed(self) -> float:
        return self.api.wbu_driver_get_current_speed()

    @property
    def target_cruising_speed(self) -> float:
        return self.api.wbu_driver_get_target_cruising_speed()

    @target_cruising_speed.setter
    def target_cruising_speed(self, target_cruising_speed: float):
        self.api.wbu_driver_set_cruising_speed(ctypes.c_double(target_cruising_speed))

    @property
    def throttle(self) -> float:
        return self.api.wbu_driver_get_throttle()

    @throttle.setter
    def throttle(self, throttle: float):
        self.api.wbu_driver_set_throttle(ctypes.c_double(throttle))
