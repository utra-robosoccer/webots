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

import ctypes
import sys
from controller.wb import wb
from controller.device import Device
from controller.accelerometer import Accelerometer
from controller.altimeter import Altimeter
from controller.brake import Brake
from controller.camera import Camera
from controller.compass import Compass
from controller.connector import Connector
from controller.display import Display
from controller.distance_sensor import DistanceSensor
from controller.emitter import Emitter
from controller.gps import GPS
from controller.gyro import Gyro
from controller.inertial_unit import InertialUnit
from controller.led import LED
from controller.lidar import Lidar
from controller.light_sensor import LightSensor
from controller.motor import Motor
from controller.pen import Pen
from controller.position_sensor import PositionSensor
from controller.radar import Radar
from controller.range_finder import RangeFinder
from controller.receiver import Receiver
from controller.skin import Skin
from controller.speaker import Speaker
from controller.touch_sensor import TouchSensor

from controller.constants import constant

from controller.joystick import Joystick
from controller.keyboard import Keyboard
from controller.mouse import Mouse


class Robot:
    EVENT_QUIT = -1
    EVENT_NO_EVENT = 0
    EVENT_MOUSE_CLICK = 1
    EVENT_MOUSE_MOVE = 2
    EVENT_KEYBOARD = 4
    EVENT_JOYSTICK_BUTTON = 8
    EVENT_JOYSTICK_AXIS = 16
    EVENT_JOYSTICK_POV = 32
    MODE_SIMULATION = 0
    MODE_CROSS_COMPILATION = 1
    MODE_REMOTE_CONTROL = 2
    created = None
    wb.wb_robot_get_name.restype = ctypes.c_char_p
    wb.wb_robot_get_model.restype = ctypes.c_char_p
    wb.wb_robot_get_custom_data.restype = ctypes.c_char_p
    wb.wb_robot_get_basic_time_step.restype = ctypes.c_double
    wb.wb_robot_get_time.restype = ctypes.c_double
    wb.wb_robot_get_name.restype = ctypes.c_char_p
    wb.wb_robot_battery_sensor_get_value.restype = ctypes.c_double

    def __init__(self):
        if Robot.created:
            print('Error: only one Robot instance can be created per controller process.', file=sys.stderr)
            return
        Robot.created = self
        wb.wb_robot_init()
        self.NODE_ACCELEROMETER = constant('NODE_ACCELEROMETER')
        self.NODE_ALTIMETER = constant('NODE_ALTIMETER')
        self.NODE_BRAKE = constant('NODE_BRAKE')
        self.NODE_CAMERA = constant('NODE_CAMERA')
        self.NODE_COMPASS = constant('NODE_COMPASS')
        self.NODE_CONNECTOR = constant('NODE_CONNECTOR')
        self.NODE_DISPLAY = constant('NODE_DISPLAY')
        self.NODE_DISTANCE_SENSOR = constant('NODE_DISTANCE_SENSOR')
        self.NODE_EMITTER = constant('NODE_EMITTER')
        self.NODE_GPS = constant('NODE_GPS')
        self.NODE_GYRO = constant('NODE_GYRO')
        self.NODE_INERTIAL_UNIT = constant('NODE_INERTIAL_UNIT')
        self.NODE_LED = constant('NODE_LED')
        self.NODE_LIDAR = constant('NODE_LIDAR')
        self.NODE_LIGHT_SENSOR = constant('NODE_LIGHT_SENSOR')
        self.NODE_LINEAR_MOTOR = constant('NODE_LINEAR_MOTOR')
        self.NODE_PEN = constant('NODE_PEN')
        self.NODE_POSITION_SENSOR = constant('NODE_POSITION_SENSOR')
        self.NODE_RADAR = constant('NODE_RADAR')
        self.NODE_RANGE_FINDER = constant('NODE_RANGE_FINDER')
        self.NODE_RECEIVER = constant('NODE_RECEIVER')
        self.NODE_ROTATIONAL_MOTOR = constant('NODE_ROTATIONAL_MOTOR')
        self.NODE_SKIN = constant('NODE_SKIN')
        self.NODE_SPEAKER = constant('NODE_SPEAKER')
        self.NODE_TOUCH_SENSOR = constant('NODE_TOUCH_SENSOR')
        self.devices = {}
        n = wb.wb_robot_get_number_of_devices()
        for i in range(0, n):
            tag = wb.wb_robot_get_device_by_index(i)
            name = wb.wb_device_get_name(tag).decode()
            type = wb.wb_device_get_node_type(tag)
            if type == self.NODE_ACCELEROMETER:
                self.devices[name] = Accelerometer(tag)
            elif type == self.NODE_ALTIMETER:
                self.devices[name] = Altimeter(name)
            elif type == self.NODE_BRAKE:
                self.devices[name] = Brake(tag)
            elif type == self.NODE_CAMERA:
                self.devices[name] = Camera(tag)
            elif type == self.NODE_COMPASS:
                self.devices[name] = Compass(tag)
            elif type == self.NODE_CONNECTOR:
                self.devices[name] = Connector(tag)
            elif type == self.NODE_DISPLAY:
                self.devices[name] = Display(tag)
            elif type == self.NODE_DISTANCE_SENSOR:
                self.devices[name] = DistanceSensor(tag)
            elif type == self.NODE_EMITTER:
                self.devices[name] = Emitter(tag)
            elif type == self.NODE_GPS:
                self.devices[name] = GPS(tag)
            elif type == self.NODE_GYRO:
                self.devices[name] = Gyro(tag)
            elif type == self.NODE_INERTIAL_UNIT:
                self.devices[name] = InertialUnit(tag)
            elif type == self.NODE_LED:
                self.devices[name] = LED(tag)
            elif type == self.NODE_LIDAR:
                self.devices[name] = Lidar(tag)
            elif type == self.NODE_LIGHT_SENSOR:
                self.devices[name] = LightSensor(tag)
            elif type == self.NODE_LINEAR_MOTOR or type == self.NODE_ROTATIONAL_MOTOR:
                self.devices[name] = Motor(tag)
            elif type == self.NODE_PEN:
                self.devices[name] = Pen(tag)
            elif type == self.NODE_POSITION_SENSOR:
                self.devices[name] = PositionSensor(tag)
            elif type == self.NODE_RADAR:
                self.devices[name] = Radar(tag)
            elif type == self.NODE_RANGE_FINDER:
                self.devices[name] = RangeFinder(tag)
            elif type == self.NODE_RECEIVER:
                self.devices[name] = Receiver(tag)
            elif type == self.NODE_SKIN:
                self.devices[name] = Skin(tag)
            elif type == self.NODE_SPEAKER:
                self.devices[name] = Speaker(tag)
            elif type == self.NODE_TOUCH_SENSOR:
                self.devices[name] = TouchSensor(tag)
            else:
                print('Unsupported device type: ' + str(type) + ' for device named "' + name + '"', file=sys.stderr)
        self.keyboard = Keyboard(0)
        self.mouse = Mouse(0)
        self.joystick = Joystick(0)

    def __del__(self):
        wb.wb_robot_cleanup()

    def getAccelerometer(self, name: str) -> Accelerometer:
        print('DEPRECATION: Robot.getAccelerometer is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getAltimeter(self, name: str) -> Altimeter:
        print('DEPRECATION: Robot.getAltimeter is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getBrake(self, name: str) -> Brake:
        print('DEPRECATION: Robot.getBrake is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getCamera(self, name: str) -> Camera:
        print('DEPRECATION: Robot.getCamera is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getCompass(self, name: str) -> Compass:
        print('DEPRECATION: Robot.getCompass is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getConnector(self, name: str) -> Connector:
        print('DEPRECATION: Robot.getConnector is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getDisplay(self, name: str) -> Display:
        print('DEPRECATION: Robot.getDisplay is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getDistanceSensor(self, name: str) -> DistanceSensor:
        print('DEPRECATION: Robot.getDistanceSensor is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getEmitter(self, name: str) -> Emitter:
        print('DEPRECATION: Robot.getEmitter is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getGPS(self, name: str) -> GPS:
        print('DEPRECATION: Robot.getGPS is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getGyro(self, name: str) -> Gyro:
        print('DEPRECATION: Robot.getGyro is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getInertialUnit(self, name: str) -> InertialUnit:
        print('DEPRECATION: Robot.getInertialUnit is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getLED(self, name: str) -> LED:
        print('DEPRECATION: Robot.getLed is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getLidar(self, name: str) -> Lidar:
        print('DEPRECATION: Robot.getLidar is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getLightSensor(self, name: str) -> LightSensor:
        print('DEPRECATION: Robot.getLightSensor is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getMotor(self, name: str) -> Motor:
        print('DEPRECATION: Robot.getMotor is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getPen(self, name: str) -> Pen:
        print('DEPRECATION: Robot.getPen is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getPositionSensor(self, name: str) -> PositionSensor:
        print('DEPRECATION: Robot.getPositionSensor is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getRadar(self, name: str) -> Radar:
        print('DEPRECATION: Robot.getRadar is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getRangeFinder(self, name: str) -> RangeFinder:
        print('DEPRECATION: Robot.getRangeFinder is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getReceiver(self, name: str) -> Receiver:
        print('DEPRECATION: Robot.getReceiver is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getSkin(self, name: str) -> Skin:
        print('DEPRECATION: Robot.getSkin is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getSpeaker(self, name: str) -> Speaker:
        print('DEPRECATION: Robot.getSpeaker is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getTouchSensor(self, name: str) -> TouchSensor:
        print('DEPRECATION: Robot.getTouchSensor is deprecated, please use Robot.getDevice instead.', file=sys.stderr)
        return self.getDevice(name)

    def getDevice(self, name: str) -> Device:
        if name not in self.devices:
            print(f'Device "{name}" was not found on robot "{self.name}"', file=sys.stderr)
            return None
        else:
            return self.devices[name]

    def getKeyboard(self) -> Keyboard:
        return self.keyboard

    def getMouse(self) -> Mouse:
        return self.mouse

    def getJoystick(self) -> Joystick:
        return self.joystick

    def getDeviceByIndex(self, index: int) -> Device:
        tag = wb.wb_robot_get_device_by_index(index)
        name = wb.wb_device_get_name(tag).decode()
        return self.devices[name]

    def getBasicTimeStep(self) -> float:
        return self.basic_time_step

    def getName(self) -> str:
        return self.name

    def getModel(self) -> str:
        return self.model

    def getCustomData(self) -> str:
        return self.custom_data

    def setCustomData(self, data: str):
        self.custom_data = data

    def getProjectPath(self) -> str:
        return self.project_path

    def getWorldPath(self) -> str:
        return self.world_path

    def getSupervisor(self) -> bool:
        return self.supervisor

    def getSynchronization(self) -> bool:
        return self.synchronization

    def getNumberOfDevices(self) -> int:
        return self.number_of_devices

    def getTime(self) -> float:
        return self.time

    def getUrdf(self, prefix: str) -> str:
        return wb.wb_robot_get_urdf(str.encode(prefix)).decode()

    def wwiSendText(self, text: str):
        wb.wb_robot_wwi_send_text(str.encode(text))

    def wwiReceiveText(self) -> str:
        return wb.wb_robot_wwi_receive_text().decode()

    def step(self, time_step: int = None) -> int:
        if time_step is None:
            time_step = int(self.basic_time_step)
        return wb.wb_robot_step(time_step)

    def stepBegin(self, time_step: int = None) -> int:
        if time_step is None:
            time_step = int(self.basic_time_step)
        return wb.wb_robot_step_begin(time_step)

    def stepEnd(self) -> int:
        return wb.wb_robot_step_end()

    def waitForUserInputEvent(self, event_type: int, timeout: int) -> int:
        return wb.wb_robot_wait_for_user_input_event(event_type, timeout)

    def batterySensorEnable(self, sampling_period: int):
        wb.wb_robot_battery_sensor_enable(sampling_period)

    def batterySensorDisable(self):
        wb.wb_robot_battery_sensor_disable()

    def batterySensorGetSamplingPeriod(self) -> int:
        return self.battery_sensor_sampling_period

    def batterySensorGetValue(self) -> float:
        return wb.wb_robot_battery_sensor_get_value()

    def getMode(self) -> int:
        return self.mode

    def setMode(self, mode: int, arg: str):
        wb.wb_robot_set_mode(mode, str.encode(arg))

    @property
    def basic_time_step(self) -> float:
        return wb.wb_robot_get_basic_time_step()

    @property
    def name(self) -> str:
        return wb.wb_robot_get_name().decode()

    @property
    def model(self) -> str:
        return wb.wb_robot_get_model().decode()

    @property
    def custom_data(self) -> str:
        return wb.wb_robot_get_custom_data().decode()

    @custom_data.setter
    def custom_data(self, data: str):
        wb.wb_robot_set_custom_data(str.encode(data))

    @property
    def project_path(self) -> str:
        return wb.wb_robot_get_project_path().decode()

    @property
    def world_path(self) -> str:
        return wb.wb_robot_get_world_path().decode()

    @property
    def supervisor(self) -> bool:
        return wb.wb_robot_get_supervisor() != 0

    @property
    def synchronization(self) -> bool:
        return wb.wb_robot_get_synchronization() != 0

    @property
    def time(self) -> float:
        return wb.wb_robot_get_time()

    @property
    def number_of_devices(self) -> int:
        return wb.wb_robot_get_number_of_devices()

    @property
    def battery_sensor_sampling_period(self) -> int:
        return wb.wb_robot_battery_sensor_get_sampling_period()

    @battery_sensor_sampling_period.setter
    def battery_sensor_sampling_period(self, sampling_period: int):
        if sampling_period is None:
            sampling_period = int(self.basic_time_step)
        wb.wb_robot_battery_sensor_enable(sampling_period)

    @property
    def mode(self) -> int:
        return wb.wb_robot_get_mode()
