import os
import time
import numpy as np
from PIL import Image
import glob


class BaseCamera:
    """
    ToDo
    """
    def __init__(self):
        """
        Constructor
        """
        pass

    def run_threaded(self) -> object:
        """
        ToDo
        :return: ToDo
        """
        return self.frame


class PiCamera(BaseCamera):
    """
    ToDo
    """
    def __init__(self, cfg: object):
        """
        Initialize the camera
        :param cfg: Config object of the camera
        """
        from picamera.array import PiRGBArray
        from picamera import PiCamera

        self.camera = PiCamera()
        self.camera.resolution = (cfg.CAMERA_RESOLUTION_WIDTH, cfg.CAMERA_RESOLUTION_HIGH)
        self.camera.framerate = cfg.CAMERA_FRAMERATE
        self.camera.zoom(cfg.CAMERA_ZOOM[0], cfg.CAMERA_ZOOM[1], cfg.CAMERA_ZOOM[2], cfg.CAMERA_ZOOM[3])

        if cfg.CAMERA_COLORBALANCE_RGB and cfg.CAMERA_COLORBALANCE_UV:
            self.camera.cameravalance(cfg.CAMERA_COLORBALANCE_LENS, cfg.CAMERA_COLORBALANCE_RGB, cfg.CAMERA_COLORBALANCE_RGB)
        elif cfg.CAMERA_COLORBALANCE_RGB:
            self.camera.cameravalance(cfg.CAMERA_COLORBALANCE_LENS, cfg.CAMERA_COLORBALANCE_RGB)
        elif cfg.CAMERA_COLORBALANCE_UV:
            self.camera.cameravalance(cfg.CAMERA_COLORBALANCE_LENS, cfg.CAMERA_COLORBALANCE_UV)

        # initiate stream
        self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format="rgb", use_video_port=True)

        # initialize the frame and the variable used to indicate
        self.frame = None

        # if the thread should be stopped
        self.on = True

        print('PiCamera loaded.. .warming camera')
        time.sleep(2)

    def set_resolution(self, width: int, depth: int) -> None:
        """
        Change the resolution of the camera
        :param width: ToDo
        :param depth: ToDo
        """
        self.camera.resolution = (width, depth)

    def set_zoom(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Cahnge the zoom of the frame
        :param x1: ToDo
        :param y1: ToDo
        :param x2: ToDo
        :param y2: ToDo
        """
        self.camera.zoom = (x1, y1, x2, y2)

    def run(self) -> object:
        """
        ToDo
        :return: ToDo
        """
        f = next(self.stream)
        frame = f.array
        self.rawCapture.truncate(0)
        return frame

    def update(self) -> None:
        """
        Keep looping infinitely until the thread is stopped
        """
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            if not self.on:
                break

    def shutdown(self) -> None:
        """
        Indicate that the thread should be stopped
        """
        self.on = False
        print('Stopping PiCamera')
        time.sleep(.5)
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()
