"""
CAR CONFIG

This file is read by your car application's manage.py script to change the car
performance.

EXMAPLE
-----------
import dk
cfg = dk.load_config(config_path='~/mycar/config.py')
print(cfg.CAMERA_RESOLUTION)

"""


import os

############################## 
# PATHS 
##############################
CAR_PATH = PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(CAR_PATH, 'data')
MODELS_PATH = os.path.join(CAR_PATH, 'models')

############################## 
# VEHICLE 
##############################
DRIVE_LOOP_HZ = 20
MAX_LOOPS = 100000

############################## 
# CAMERA 
# https://picamera.readthedocs.io/en/release-1.13/recipes1.html
##############################
CAMERA_RESOLUTION_HIGH = 120
CAMERA_RESOLUTION_WIDTH = 160
CAMERA_FRAMERATE = 20
CAMERA_ZOOM = (0, 0, 1, 1)
CAMERA_COLORBALANCE_LENS = 0
CAMERA_COLORBALANCE_RGB = None
CAMERA_COLORBALANCE_UV = None

##############################
#STEERING
##############################
STEERING_CHANNEL = 1
STEERING_LEFT_PWM = 420
STEERING_RIGHT_PWM = 360

##############################
#THROTTLE
##############################
THROTTLE_CHANNEL = 0
THROTTLE_FORWARD_PWM = 400
THROTTLE_STOPPED_PWM = 360
THROTTLE_REVERSE_PWM = 310

##############################
#TRAINING
##############################
BATCH_SIZE = 128
TRAIN_TEST_SPLIT = 0.8

##############################
#JOYSTICK
##############################
USE_JOYSTICK_AS_DEFAULT = False
JOYSTICK_MAX_THROTTLE = 0.25
JOYSTICK_STEERING_SCALE = 1.0
AUTO_RECORD_ON_THROTTLE = True

# if using a single tub
TUB_PATH = os.path.join(CAR_PATH, 'tub') 
