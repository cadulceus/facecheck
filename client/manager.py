from Crypto.Cipher import AES
import cv2, json

class Vault(object):
    SECRET_HEADER = "===========BEGIN SECRET==========="
    SECRET_FOOTER = "============END SECRET============"
    TRAINING_HEADER = "===========BEGIN TRAINING==========="
    TRAINING_FOOTER = "============END TRAINING============"
    DATA_HEADER = "===========BEGIN DATA==========="
    DATA_FOOTER = "============END DATA============"
    CHECKSUM = "FCHK" * 8
    IV = "1616161616161616"
    def __init__(self):
        self.filename = ""
        self.pin = ""
        self.first = True
        self.secret = ""
        self.encrypted_secret = ""
        self.encrypted_training = ""
        self.encrypted_data = ""
        self.training = {}
        self.items = {}
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

        return True

    def load(self):
        with open(self.filename, 'r') as r:
            data = r.read()

        return self._deserialize(data)


    def train(self):
        return

    def lock(self):
        self.secret = ""
        self.items = []

    def unlock(self):
        pin = self._pad(self.pin)

        if self.first:
            obj = AES.new(pin, AES.MODE_CBC, Vault.IV)
            self.secret = obj.decrypt(self.encrypted_secret)
            if not self.secret.startswith(Vault.CHECKSUM):
                return False
            self.secret = self.secret[len(Vault.CHECKSUM):].rstrip('\x00')

        key = self._pad(self._make_key())

        if self.first:
            obj = AES.new(key, AES.MODE_CBC, pin)
            tmp_training = obj.decrypt(self.encrypted_training)
            if not tmp_training.startswith(Vault.CHECKSUM):
                return False
            tmp_training = tmp_training[len(Vault.CHECKSUM):].rstrip('\x00')
            self.training = json.loads(tmp_training)
            self.train()


        obj = AES.new(key, AES.MODE_CBC, pin)
        tmp_items = obj.decrypt(self.encrypted_data)
        if not tmp_items.startswith(Vault.CHECKSUM):
            return False
        tmp_items = tmp_items[len(Vault.CHECKSUM):].rstrip('\x00')
        self.items = json.loads(tmp_items)

        self.first = False

        return True
    
    def save(self):
        with open(self.filename, 'w') as w:
            w.write(self._serialize())

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

    print "Trying file save to {}".format(v.filename)
    v.save()

    v.secret = ""
    v.training = None
    v.items = None
    print "Trying file load from {}".format(v.filename)
    print v.load()
    print v.unlock()
    print v.secret == secret
    print "Loaded secret: {}".format(v.secret)
    print "Loaded training set: {}".format(v.training)
    print "Loaded data set: {}".format(v.items)

if __name__ == '__main__':
    main()
