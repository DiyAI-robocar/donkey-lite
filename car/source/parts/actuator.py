"""
Classes to control the motors and servos. These classes
are wrapped in a mixer class before being used in the drive loop.
"""

import time
from ..util import data


class PCA9685:
    """
    PWM motor controller using PCA9685 boards.
    This is used for most RC Cars
    """
    def __init__(self, channel: int, frequency: int=60):
        """
        Constructor
        :param channel:
        :param frequency:
        """
        import Adafruit_PCA9685
        # Initialise the PCA9685 using the default address (0x40).
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(frequency)
        self.channel = channel

    def set_pulse(self, pulse: int) -> None:
        """
        Sets a single PWM channel.
        :param pulse:
        """
        self.pwm.set_pwm(self.channel, 0, pulse)

    def run(self, pulse: int) -> None:
        """
        ToDo
        :param pulse: ToDo
        """
        self.set_pulse(pulse)


class PWMSteering:
    """
    Wrapper over a PWM motor controller to convert angles to PWM pulses.
    """
    LEFT_ANGLE = -1
    RIGHT_ANGLE = 1

    class Settings:
        inputs = ['angle']
        left_pulse = 290
        right_pulse = 490

    def __init__(self, controller=None, left_pulse: int=290, right_pulse: int=490):
        """
        Constructor
        :param controller:
        :param left_pulse:
        :param right_pulse:
        """
        self.controller = controller
        self.left_pulse = left_pulse
        self.right_pulse = right_pulse

    def run(self, angle: int) -> None:
        """
        Map absolute angle to angle that vehicle can implement.
        :param angle: ToDo
        """
        pulse = data.map_range(angle, self.LEFT_ANGLE, self.RIGHT_ANGLE, self.left_pulse, self.right_pulse)
        self.controller.set_pulse(pulse)

    def shutdown(self) -> None:
        """
        Set steering straight
        """
        self.run(0)


class PWMThrottle:
    """
    Wrapper over a PWM motor cotnroller to convert -1 to 1 throttle
    values to PWM pulses.
    """
    MIN_THROTTLE = -1
    MAX_THROTTLE = 1

    def __init__(self, controller=None, max_pulse: int=300, min_pulse: int=490, zero_pulse: int=350):
        """
        Constructor
        :param controller:
        :param max_pulse:
        :param min_pulse:
        :param zero_pulse:
        """
        self.controller = controller
        self.max_pulse = max_pulse
        self.min_pulse = min_pulse
        self.zero_pulse = zero_pulse

        # send zero pulse to calibrate ESC
        self.controller.set_pulse(self.zero_pulse)
        time.sleep(1)

    def run(self, throttle: int) -> None:
        """
        ToDo
        :param throttle: ToDo
        :return: ToDo
        """
        if throttle > 0:
            pulse = data.map_range(throttle, 0, self.MAX_THROTTLE, self.zero_pulse, self.max_pulse)
        else:
            pulse = data.map_range(throttle, self.MIN_THROTTLE, 0, self.min_pulse, self.zero_pulse)

        self.controller.set_pulse(pulse)

    def shutdown(self) -> None:
        """
        Stop vehicle
        """
        self.run(0)


class Adafruit_DCMotor_Hat:
    """
    Adafruit DC Motor Controller
    Used for each motor on a differential drive car.
    """
    def __init__(self, motor_num):
        from Adafruit_MotorHAT import Adafruit_MotorHAT
        import atexit

        self.FORWARD = Adafruit_MotorHAT.FORWARD
        self.BACKWARD = Adafruit_MotorHAT.BACKWARD
        self.mh = Adafruit_MotorHAT(addr=0x60)

        self.motor = self.mh.getMotor(motor_num)
        self.motor_num = motor_num

        atexit.register(self.turn_off_motors)
        self.speed = 0
        self.throttle = 0

    def run(self, speed: float) -> None:
        """
        Update the speed of the motor where 1 is full forward and -1 is full backwards.
        :param speed: ToDo
        """
        if speed > 1 or speed < -1:
            raise ValueError("Speed must be between 1(forward) and -1(reverse)")

        self.speed = speed
        self.throttle = int(data.map_range(abs(speed), -1, 1, -255, 255))

        if speed > 0:
            self.motor.run(self.FORWARD)
        else:
            self.motor.run(self.BACKWARD)

        self.motor.setSpeed(self.throttle)

    def shutdown(self) -> None:
        """
        ToDo
        """
        self.mh.getMotor(self.motor_num).run(Adafruit_MotorHAT.RELEASE)
