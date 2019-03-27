import cv2

def diffImg(t0,t1, t2):
	d1 = cv2.absdiff(t2,t1)
	d2 = cv2.absdiff(t1, t0)
	return cv2.bitwise_and(d1,d2)

def show_webcam(mirror=False):
	cam = cv2.VideoCapture(0)
	cam.set(cv2.CAP_PROP_FPS, 16)
	cam.set(3, 1024)
	cam.set(4, 768)
	#Read three images first
	t_minus = None
	frame = None
	while True:
		if not cam.isOpened():
			print("[ERROR] camera is not open.")
			break

		if t_minus is None:
			t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
			t_minus = cv2.GaussianBlur(t_minus, (5,5),0)
			t = t_minus.copy()
			t_plus = t_minus.copy()
			continue
		if frame is None:
			frame = cam.read()[1]
			frame_plus = frame.copy()
			continue

		frameDelta = diffImg(t_minus, t, t_plus)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=1)
		cnts,hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		for c in cnts:
			#if the contour is too small, ignore it
			if cv2.contourArea(c) < 5:
				continue
			(x,y,w,h) = cv2.boundingRect(c)
			cv2.putText(frame, 'Mouvement', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)

		if mirror:
			frame = cv2.flip(img, 1)
		cv2.imshow('my webcam', frame)

		t_minus = t
		t = t_plus
		t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
		t_plus = cv2.GaussianBlur(t_plus, (5,5), 0)
		frame = frame_plus
		frame_plus = cam.read()[1]

		if cv2.waitKey(1) == 27:
			break
	cv2.destroyAllWindows()

def main():
	show_webcam()

if __name__ == '__main__':
	main()