
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from libcamera import controls

class CameraHandler:
    def __init__(self):
        self.init_camera()

    def init_camera(self):
        self.picam2 = Picamera2()
        self.config = self.picam2.create_preview_configuration()
        self.picam2.configure(self.config)
        self.picam2.start()
        self.encoder = H264Encoder(bitrate=2500000)
        self.recording = False
        self.initialized = True

    def start_recording(self, filename):
        output = FfmpegOutput(filename)
        self.picam2.start_recording(self.encoder, output)
        self.recording = True

    def stop_recording(self):
        self.picam2.stop_recording()
        self.picam2.close()
        self.recording = False
        self.initialized = False

    def cap_frame(self):
        return self.picam2.capture_array()

