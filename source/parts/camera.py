import os
import time
import numpy as np
from PIL import Image
import glob


class BaseCamera:

    def run_threaded(self):
        return self.frame


class PiCamera(BaseCamera):
    def __init__(self, resolution=(120, 160), framerate=20, zoom=(0, 0, 1, 1)):
        from picamera.array import PiRGBArray
        from picamera import PiCamera

        # initialize the camera
        self.camera = PiCamera()
        self.camera.resolution = (resolution[1], resolution[0])
        self.camera.framerate = framerate
        self.camera.zoom(zoom[0], zoom[1], zoom[2], zoom[3])

        if(cfg.CAMERA_COLORBALANCE_RGB and  cfg.CAMERA_COLORBALANCE_UV):
            self.camera.cameravalance(cfg.CAMERA_COLORBALANCE_LENS, cfg.CAMERA_COLORBALANCE_RGB, cfg.CAMERA_COLORBALANCE_RGB)            
        elif(cfg.CAMERA_COLORBALANCE_RGB):
            self.camera.cameravalance(cfg.CAMERA_COLORBALANCE_LENS, cfg.CAMERA_COLORBALANCE_RGB)
        elif(cfg.CAMERA_COLORBALANCE_UV):
            self.camera.cameravalance(cfg.CAMERA_COLORBALANCE_LENS, cfg.CAMERA_COLORBALANCE_UV)

        # initiate stream
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
                                                     format="rgb",
                                                     use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.on = True

        print('PiCamera loaded.. .warming camera')
        time.sleep(2)

    def run(self):
        f = next(self.stream)
        frame = f.array
        self.rawCapture.truncate(0)
        return frame

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            if not self.on:
                break

    def shutdown(self):
        # indicate that the thread should be stopped
        self.on = False
        print('stoping PiCamera')
        time.sleep(.5)
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()
