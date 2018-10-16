# -*- coding: utf-8 -*-

import time


class Lambda:
    """
    Wraps a function into a donkey part.
    """
    def __init__(self, f):
        """
        Constructor
        :param f: function to use
        """
        self.f = f

    def run(self, *args, **kwargs) -> object:
        """
        Execute the saved function
        :param args: ToDo
        :param kwargs: ToDo
        :return: ToDo
        """
        return self.f(*args, **kwargs)

    def shutdown(self) -> None:
        """
        ToDo
        """
        pass


class PIDController:
    """
    Performs a PID computation and returns a control value.
    This is based on the elapsed time (dt) and the current value of the process variable
    (i.e. the thing we're measuring and trying to change).
    https://github.com/chrisspen/pid_controller/blob/master/pid_controller/pid.py
    """

    def __init__(self, p: int=0, i: int=0, d: int=0, debug:bool=False):
        """
        Constructor, initialize gains
        :param p: ToDo
        :param i: ToDo
        :param d: ToDo
        :param debug: ToDo
        """
        self.Kp = p
        self.Ki = i
        self.Kd = d

        # The value the controller is trying to get the system to achieve.
        self.target = 0

        # initialize delta t variables
        self.prev_tm = time.time()
        self.prev_feedback = 0
        self.error = None

        # initialize the output
        self.alpha = 0

        # debug flag (set to True for console output)
        self.debug = debug

    def run(self, target_value: int, feedback: int) -> int:
        """
        ToDo
        :param target_value: ToDo
        :param feedback: ToDo
        :return: ToDo
        """
        curr_tm = time.time()

        self.target = target_value
        error = self.error = self.target - feedback

        # Calculate time differential.
        dt = curr_tm - self.prev_tm

        # Initialize output variable.
        curr_alpha = 0

        # Add proportional component.
        curr_alpha += self.Kp * error

        # Add integral component.
        curr_alpha += self.Ki * (error * dt)

        # Add differential component (avoiding divide-by-zero).
        if dt > 0:
            curr_alpha += self.Kd * ((feedback - self.prev_feedback) / float(dt))

        # Maintain memory for next loop.
        self.prev_tm = curr_tm
        self.prev_feedback = feedback

        # Update the output
        self.alpha = curr_alpha

        if (self.debug):
            print('PID target value:', round(target_value, 4))
            print('PID feedback value:', round(feedback, 4))
            print('PID output:', round(curr_alpha, 4))

        return curr_alpha
