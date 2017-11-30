from Crypto.Cipher import AES
from tempfile import TemporaryFile
import cv2, datetime, hashlib, json
import numpy as np

class Vault(object):
    SECRET_HEADER = "===========BEGIN SECRET==========="
    SECRET_FOOTER = "============END SECRET============"
    TRAINING_HEADER = "===========BEGIN TRAINING==========="
    TRAINING_FOOTER = "============END TRAINING============"
    DATA_HEADER = "===========BEGIN DATA==========="
    DATA_FOOTER = "============END DATA============"
    CHECKSUM = "FCHK" * 8
    IV = "1616161616161616"
    DESIRED_LABEL = int(hashlib.md5("user").hexdigest(), 16) % (2 ** 31) # replace with data recieved from plugin?
    def __init__(self):
        self.filename = ""
        self.pin = ""
        self.unlocked = False
        self.first = True
        self.secret = ""
        self.encrypted_secret = ""
        self.encrypted_training = ""
        self.encrypted_data = ""
        self.training = {}
        self.items = {}
        self.labels = np.array([])
        self.images = []
        try:
            recognizer = cv2.face.createLBPHFaceRecognizer()
        except:
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()


    def _pad(self, s, char='\x00', length=16):
        s += char * (length - (len(s) % length))
        return s

    def _make_key(self):
        tmp = self.secret[len(Vault.CHECKSUM):].rstrip('\x00')
        key = ""
        for word in self.secret.split():
            total = sum([ord(c) for c in word])
            key += chr(total % 256)

        return key

    def _serialize(self):
        pin = self._pad(self.pin)
        obj = AES.new(pin, AES.MODE_CBC, Vault.IV)
        encrypted_secret = obj.encrypt(self._pad(Vault.CHECKSUM + self.secret))

        key = self._pad(self._make_key())
        obj = AES.new(key, AES.MODE_CBC, pin)
        encrypted_training = obj.encrypt(self._pad(Vault.CHECKSUM + json.dumps(self.training)))

        obj = AES.new(key, AES.MODE_CBC, pin)
        encrypted_data = obj.encrypt(self._pad(Vault.CHECKSUM + json.dumps(self.items)))

        s = "\n".join([Vault.SECRET_HEADER,
                       encrypted_secret,
                       Vault.SECRET_FOOTER,
                       Vault.TRAINING_HEADER,
                       encrypted_training,
                       Vault.TRAINING_FOOTER,
                       Vault.DATA_HEADER,
                       encrypted_data,
                       Vault.DATA_FOOTER])

        return s

    def _deserialize(self, data):
        sec_start = data.find(Vault.SECRET_HEADER)
        sec_end = data.find(Vault.SECRET_FOOTER)
        if sec_start == -1 or sec_end == -1:
            return False
        sec_start += len(Vault.SECRET_HEADER)

        data_start = data.find(Vault.DATA_HEADER)
        data_end = data.find(Vault.DATA_FOOTER)
        if data_start == -1 or data_end == -1:
            return False
        data_start += len(Vault.DATA_HEADER)

        training_start = data.find(Vault.TRAINING_HEADER)
        training_end = data.find(Vault.TRAINING_FOOTER)
        if data_start == -1 or training_end == -1:
            return False
        training_start += len(Vault.TRAINING_HEADER)

        self.encrypted_secret = data[sec_start + 1:sec_end - 1]
        self.encrypted_data = data[data_start + 1:data_end - 1]
        self.encrypted_training = data[training_start + 1:training_end - 1]

        #print self.encrypted_secret
        #print self.encrypted_data 
        #print self.encrypted_training
        return True

    def load(self):
        with open(self.filename, 'r') as r:
            data = r.read()
        
        return self._deserialize(data)


    def train(self):
        return

    def lock(self):
        self.secret = ""
        self.items = {}
        self.unlocked = False

    def unlock(self):
        pin = self._pad(self.pin)

        if self.first or not self.secret:
            obj = AES.new(pin, AES.MODE_CBC, Vault.IV)
            self.secret = obj.decrypt(self.encrypted_secret)
            if not self.secret.startswith(Vault.CHECKSUM):
                return False
            self.secret = self.secret[len(Vault.CHECKSUM):].rstrip('\x00')


        key = self._pad(self._make_key())

        obj = AES.new(key, AES.MODE_CBC, pin)
        tmp_training = obj.decrypt(self.encrypted_training)
        if not tmp_training.startswith(Vault.CHECKSUM):
            return False
        tmp_training = tmp_training[len(Vault.CHECKSUM):].rstrip('\x00')
        self.training = json.loads(tmp_training)

        try:
            outfile = TemporaryFile()
            outfile.write(self.training['images'].decode('base64'))
            outfile.seek(0)
            self.images = np.load(outfile)
        except:
            print "Failed to load saved numpy array"

        try:
            outfile = TemporaryFile()
            outfile.write(self.training['labels'].decode('base64'))
            outfile.seek(0)
            self.labels = np.load(outfile)
        except:
            print "Failed to load saved numpy array"
        if self.first:
            self.train()


        obj = AES.new(key, AES.MODE_CBC, pin)
        tmp_items = obj.decrypt(self.encrypted_data)
        if not tmp_items.startswith(Vault.CHECKSUM):
            return False
        tmp_items = tmp_items[len(Vault.CHECKSUM):].rstrip('\x00')
        self.items = json.loads(tmp_items)

        self.first = False
        self.unlocked = True

        return True

    def add_item(self, service, entry_name, username, password):
        if not self.unlocked:
            return False

        if service not in self.items:
            self.items[service] = []
        
        h = hashlib.sha512()
        h.update(service + entry_name + str(datetime.datetime.utcnow()))
        new_item = {'username': username,
                    'password': password,
                    'name': entry_name,
                    'id': h.hexdigest()}

        self.items[service].append(new_item) 
        return new_item

    def edit_item(self, service, password):
        if not self.unlocked or service not in self.items:
            return False
        
        self.items[service][0]['password'] = password
        return modified
    
    def save(self):
        with open(self.filename, 'w') as w:
            w.write(self._serialize())

    def extract_face(self, gs, face_cascade):
            faces = face_cascade.detectMultiScale(gs, minSize=(75,75))
            for (x, y, w, h) in faces:
                    #cv2.rectangle(gs, (x,y),(x+w,y+h), (255, 0, 0), 2)
                    #cv2.imshow("Added face", gs)
                    return gs[y: y + h, x: x + w]

    def detect(self, threshold=20, confidence_threshold = 50):
        video_capture = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        for i in range(threshold):
            ret, frame = video_capture.read()
            gs = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            found_face = self.extract_face(gs, face_cascade)
            try:
                nbr_predicted, conf = self.recognizer.predict(found_face)
            except Exception:
                print Exception
                print "Probably couldn't find a face"
                continue
            print "Label: ", nbr_predicted
            print "Confidence: ", conf
            if conf < confidence_threshold:
                return True

        return False


    def train(self):
        self.recognizer.train(self.images, self.labels)

    def collect_faces(self, threshold=20):
            video_capture = cv2.VideoCapture(0)
            old_len = len(self.images)
            face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            new_adds = 0
            while new_adds < threshold:
                    ret, frame = video_capture.read()
                    #cv2.imshow("Added face", frame)
                    gs = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    found_face = self.extract_face(gs, face_cascade)
                    if  isinstance(found_face, type(None)) or not found_face.all():
                        continue
                    self.images.append(found_face)
                    new_adds += 1
                    #cv2.imshow("Added face", images[-1])
                    #cv2.waitKey(threshold)
            #label is an identifier for an individual face
            print "Found " + str(len(self.images)) + " faces"
            tmp = self.labels
            if len(self.labels) == 0:
                    self.labels = np.asarray([Vault.DESIRED_LABEL for i in range(len(self.images)-old_len)], dtype="int")
            else:
                    self.labels = np.asarray(tmp, np.array([Vault.DESIRED_LABEL for i in range(len(self.images)-old_len)]), dtype="int")

            outfile = TemporaryFile()
            np.save(outfile, self.images)
            outfile.seek(0)
            self.training['images'] = outfile.read().encode('base64')

            outfile = TemporaryFile()
            np.save(outfile, self.labels)
            outfile.seek(0)
            self.training['labels'] = outfile.read().encode('base64')

def main():
    v = Vault()
    v.filename = "test.fcvault"
    v.pin = "1234"
    wordlist = "words.txt"
    with open(wordlist, 'r') as r:
        words = [w.strip() for w in r.readlines()]

    import random 
    secret = ' '.join([random.choice(words) for i in xrange(10)])
    test_training = {'images': [['image data', 'label1'], ['image data 2', 'label2']]}
    test_data = {"items": [{"username": "abc", "password": "123", "domain": "test.com"},
                           {"username": "xyz", "password": "789", "domain": "test2.com"}]}

    v.secret = secret
    v.training = test_training
    v.items = test_data

    print "Generated secret: {}".format(secret)
    print "Using test training set: {}".format(test_training)
    print "Using test data set: {}".format(test_data)

    v.collect_faces()
    v.train()
    print v.images
    print v.labels
    print v.training
    print v.detect()
    tmp_img = v.images
    tmp_lbl = v.labels

    print "Trying file save to {}".format(v.filename)
    v.save()

    v.secret = ""
    v.training = None
    v.items = None
    print "Trying file load from {}".format(v.filename)
    print v.load()
    print v.unlock()
    print v.secret == secret
    print tmp_img == v.images
    print tmp_lbl == v.labels
    print v.detect()
    print "Loaded secret: {}".format(v.secret)
    print "Loaded data set: {}".format(v.items)

if __name__ == '__main__':
    main()
