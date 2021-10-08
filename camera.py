import cv2

class Video(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__ (self):
        self.video.release()
    
    def gen_frames(self):

        success, frame = self.video.read()
        ret, jpg = cv2.imencode(".jpg", frame=frame)
        return jpg.tobytes()