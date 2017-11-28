import cv2, hashlib
import numpy as np

#prereqs: opencv-python version 3.1, opencv-contrib-python version 3.2.0.7, numpy

"""Takes a greyscale image, returns a numpy array as the sub image of the argument containing a face"""
def extract_face(gs, face_cascade):
	faces = face_cascade.detectMultiScale(gs, minSize=(75,75))
	for (x, y, w, h) in faces:
                cv2.rectangle(gs, (x,y),(x+w,y+h), (255, 0, 0), 2)
		cv2.imshow("Added face", gs)
		return gs[y: y + h, x: x + w]

def detect(recognizer):
	video_capture = cv2.VideoCapture(0)
	face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	for i in range(15):
		ret, frame = video_capture.read()
		gs = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		found_face = extract_face(gs, face_cascade)
		try:
			nbr_predicted, conf = recognizer.predict(found_face)
		except Exception:
			print Exception
			print "Probably couldn't find a face"
			continue
		print "Label: ", nbr_predicted
		print "Confidence: ", conf


def train(recognizer, images, labels):
	recognizer.train(images, labels)

def collect_faces(images, labels, inp_count, recognizer, desired_label):
	video_capture = cv2.VideoCapture(0)
	old_len = len(images)
	face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	for i in range(inp_count):
		ret, frame = video_capture.read()
		#cv2.imshow("Added face", frame)
		gs = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		found_face = extract_face(gs, face_cascade)
		if not found_face.all():
			continue;
		images.append(found_face)
		#cv2.imshow("Added face", images[-1])
		cv2.waitKey(inp_count)
	#label is an identifier for an individual face
	print "Found " + str(len(images)) + " faces"
	tmp = labels
	if len(labels) == 0:
		labels = np.asarray([desired_label for i in range(len(images)-old_len)], dtype="int")
	else:
		labels = np.asarray(tmp, np.array([desired_label for i in range(len(images)-old_len)]), dtype="int")
	return images, labels

def main():
        try:
	    recognizer = cv2.face.createLBPHFaceRecognizer()
        except:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
	labels = np.array([])
	images = []
	while 1:
		print len(images)
		print len(labels)
		print labels
		print "1: collect_faces\n2: Train\n3: Detect"
		cmd = raw_input()
		if cmd == "1":
			print "input desired frame count"
			inp_count = int(raw_input())
			print "input name of target: "
			name = raw_input()
			desired_label = int(hashlib.md5(name).hexdigest(), 16) % (2 ** 31) # replace with data recieved from plugin?
			images, labels = collect_faces(images, labels, inp_count, recognizer, desired_label)
		elif cmd == "2":
			train(recognizer, images, labels)
		elif cmd == "3":
			detect(recognizer)
main()
