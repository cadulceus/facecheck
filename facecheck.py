import cv2, time, os
import numpy as np

#prereqs: opencv-python version 3.1, opencv-contrib-python version 3.2.0.7, numpy

"""Takes a greyscale image, returns a numpy array as the sub image of the argument containing a face"""
def extract_face(gs, face_cascade):
	faces = face_cascade.detectMultiScale(gs)
	for (x, y, w, h) in faces:
		return gs[y: y + h, x: x + w]

def detect(recognizer):
	video_capture = cv2.VideoCapture(0)
	face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	for i in range(15):
		ret, frame = video_capture.read()
		gs = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		found_face = extract_face(gs, face_cascade)
		nbr_predicted, conf = recognizer.predict(found_face)
		print "Label: ", nbr_predicted
		print "Confidence: ", conf


def train(recognizer):
	video_capture = cv2.VideoCapture(0)
	images = []
	face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	for i in range(15):
		ret, frame = video_capture.read()
		gs = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		found_face = extract_face(gs, face_cascade)
		images.append(found_face)
		cv2.imshow("Added face", images[-1])
		cv2.waitKey(15)
	#label is an identifier for an individual face
	print "Input label: ",
	label = int(raw_input())
	recognizer.train(images, np.array([label for i in range(15)]))



def main():
	recognizer = cv2.face.createLBPHFaceRecognizer()
	while 1:
		print "1: Train\n2: Detect"
		cmd = raw_input()
		if cmd == "1":
			train(recognizer)
		elif cmd == "2":
			detect(recognizer)
main()