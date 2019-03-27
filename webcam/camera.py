import cv2
from motiondetect import motionDetect


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.motion = motionDetect()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if success:
            self.motion.detect(image)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
