from Crypto.Cipher import AES, PKCS1_OAEP
from alive_progress import alive_bar
from Crypto.PublicKey import RSA
from time import sleep, time
import configctl
import grapheme
import pickle
import socket


config_file = configctl.Config('config.json')
config = config_file.load()

class ServerDictionary:
    
    def __init__(self) -> None:
        self.cache = {}
        self.loadtime = 0

# Get RSA-Crypt connection
    def connect(self):
        self.conn = socket.socket()
        private_client_key = RSA.generate(2048)
        self.conn.connect((config['dictionary']['server'], 45652))
        try:
            self.conn.send('GET_SPUB'.encode())
            public_server_key = RSA.import_key(self.recvall())
        except Exception as ex:
            print(ex)
            self.conn.close()
            exit(1)
        self.conn.send('PUB_OK'.encode())
        if self.recvall().decode() == 'GET_CPUB':
            self.conn.send(private_client_key.public_key().export_key())
            if self.recvall().decode() == 'PUB_OK':
                self.cipher_Enc = PKCS1_OAEP.new(public_server_key)
                self.cipher_Dec = PKCS1_OAEP.new(private_client_key)

        else:
            self.conn.close()


    def recvall(self):
        BUFF_SIZE = 4096  # 4 KiB
        data = b''
        while True:
            part = self.conn.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE and data:
                # either 0 or end of data
                break
        return data


    def send(self, msg: bytes) -> None:
        self.conn.sendall(self.cipher_Enc.encrypt(msg))


    def recv(self) -> bytes:
        return bytes(self.cipher_Dec.decrypt(self.recvall()))


    def auth(self) -> None:
        status = False
        self.send('START'.encode())
        if self.recv().decode() == 'WHOIS':
            self.send(config['dictionary']['userID'].encode())
            if self.recv().decode() == 'OK':
                self.send(config['dictionary']['userKey'].encode())
                if self.recv().decode() == 'OK':
                    status = True
        return status


    def split_data(self, data):
        data_list = []
        while data != b'':
            data_list.append(data[:214])
            data = data[214:]
        return len(data_list), data_list


    def send_dict(self, dictionary: dict) -> None:
        self.connect()
        if self.auth():
            self.send('SENDING'.encode())
            if self.recv().decode() == 'OK':
                data = pickle.dumps(dictionary)
                data_len, data_list = self.split_data(data)
                self.send(str(data_len).encode())
                with alive_bar(data_len, title='Sending dictionary', bar='smooth', spinner='waves', elapsed=False) as bar:
                    for part in data_list:
                        if (self.recv()).decode() == 'OK':
                            self.send(part)
                            bar()
            self.conn.close()


    def recv_dict(self) -> dict:
        dictionary = {}
        self.connect()
        if self.auth():
            self.send('RECEIVING'.encode())
            parts = []
            data_len = int((self.recv()).decode())
            with alive_bar(data_len, title='Getting dictionary', bar='smooth', spinner='waves', elapsed=False) as bar:
                for _ in range(data_len):
                    self.send('OK'.encode())
                    parts.append(self.recv())
                    bar()
            pickled_dict = b''
            for part in parts:
                pickled_dict += part    
            dictionary = pickle.loads(pickled_dict)
            self.conn.close()
        return dictionary
    

    def load(self) -> dict:
        s = int(round(time()))
        if ((s - (5 * 60)) >= self.loadtime) and (config['dictionary']['use']):
            self.loadtime = s
            self.cache = self.recv_dict()

        return self.cache


    def dump(self, dictionary) -> None:
        self.cache = dictionary
        s = int(round(time()))
        if ((s - (5 * 60)) >= self.loadtime) and (config['dictionary']['use']):
            self.loadtime = s
            self.send_dict(self.cache)
