import cv2


class motionDetect(object):
    def __init__(self):
        self.frameBase = None
        self.message = True
        self.contour = True

    def detect(self, frame):
        if self.frameBase is None:
            self.frameBase = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            self.frameBase = cv2.GaussianBlur(self.frameBase, (5, 5), 0)
        else:
            temp = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            temp = cv2.GaussianBlur(temp, (5, 5), 0)
            framedelta = cv2.absdiff(temp, self.frameBase)
            thresh = cv2.threshold(framedelta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=1)
            cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if cnts:
                self.writeMessage(cnts, frame)
                self.writeContour(cnts, frame)


    def writeMessage(self, cnts, frame):
        if len(cnts) > 10:
            cv2.putText(frame, 'Mouvement', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        else:
            cv2.putText(frame, 'No Mouvement', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    def writeContour(self, cnts, frame):
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 20:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
