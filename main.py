from camera_handler import CameraHandler
from datetime import datetime
import logging
import threading
import time
import numpy as np
import cv2

DIFF_THRESHOLD = 5 # percent
CHANGE_INTERVAL = 4 # seconds
CHANGE_STOP_THRESHOLD = 3 # N * CHANGE_INTERVAL = number of seconds of no change to wait before stopping recording

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('/home/jakob/logs/zerow-motion-cam.log')
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

def calculate_difference(image1, image2):
    grey1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    grey2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(grey1, grey2)

    _, threshold = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    diff_pct = (np.sum(threshold)/255.0)/(threshold.shape[0]*threshold.shape[1])*100

    return diff_pct

def main():
    logger.info(f'[{datetime.now()}] Initializing camera...')
    camera = CameraHandler()
    logger.info(f'[{datetime.now()}] Camera initialized')

    prev_img = None
    recording = False
    no_change_count = 0

    while True:
        logger.debug(f'[{datetime.now()}] Tick')
        if not camera.initialized:
            camera.init_camera()
        img = camera.cap_frame()

        if prev_img is not None:
            diff_pct = calculate_difference(img, prev_img)

            if diff_pct > DIFF_THRESHOLD:
                if not camera.recording:
                    datestr = datetime.now().strftime('%Y%m%d-%H%M%S')
                    logger.info(f'[{datetime.now()}] Motion Detected')
                    camera.start_recording(f'/home/jakob/Videos/{datestr}.mp4')
                no_change_count = 0
            elif camera.recording:
                no_change_count += 1
                if no_change_count >= CHANGE_STOP_THRESHOLD:
                    logger.info(f'[{datetime.now()}] Stopping Recording')
                    camera.stop_recording()
                    no_change_count = 0
        prev_img = img
        logger.debug(f'[{datetime.now()}] Tock')
        time.sleep(CHANGE_INTERVAL)

if __name__ == '__main__':
    logger.info('Starting...')
    main()

