import unittest

import pytest
from .setup import on_pi
from source.parts.camera import BaseCamera


def test_base_camera():
    cam = BaseCamera()


@pytest.mark.skipif(on_pi() == False, reason='only works on RPi')
def test_picamera():
    from source.parts.camera import PiCamera
    cfg = object(
        CAMERA_RESOLUTION_HIGH=120,
        CAMERA_RESOLUTION_WIDTH = 160,
        CAMERA_FRAMERATE = 20,
        CAMERA_ZOOM = (0, 0, 1, 1),
        CAMERA_COLORBALANCE_LENS = 0,
        CAMERA_COLORBALANCE_RGB = None,
        CAMERA_COLORBALANCE_UV = None
    )
    cam = PiCamera(cfg)
    frame = cam.run()
    #assert shape is as expected. img_array shape shows (width, height, channels)
    assert frame.shape[:2] == [cfg.CAMERA_RESOLUTION_HIGH, cfg.CAMERA_RESOLUTION_WIDTH]

