import socket
from sys import exit
from time import sleep
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.fernet import Fernet
from hashlib import md5,sha256
import binascii
import secrets

class User:
    def __init__(self,name,ip,port,passhash):
        self.NAME=name
        self.IP=ip
        self.PORT=port
        self.SOCKET=None
        self.KEYPAIR=RSA.generate(3072)
        self.PUBLIC_KEY=self.KEYPAIR.publickey()
        self.HASH=passhash
        self.CLIENT_CONN=None
        self.CLIENT_ADDR=None
        self.SESSION_KEY=""
        self.CLIENT_PUBLIC_KEY=""
        self.CLIENT_USERNAME=""
        self.ENCRYPTOR=None
        self.SESSION_ENCRYPTOR=None
        self.PUBLIC_KEY_HASH=md5(self.PUBLIC_KEY.exportKey()).hexdigest()

    def listen(self):
        try :
            self.SOCKET=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.SOCKET.bind((self.IP,self.PORT))
            self.SOCKET.listen(1)
            print(f"[+] Listening On {self.IP}:{self.PORT}")
        except Exception as e:
            print(f"[+] Failed To Bind To {self.IP}:{self.PORT}")
            self.EXIT_GRACEFULLY([self.SOCKET],-1)

    def connect(self):
        tries=0
        while True:
            tries=tries+1
            try :
                self.SOCKET=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.SOCKET.connect((self.IP,self.PORT))
                break
            except socket.error :
                print("[-] Connection Failed       ", end='\r\r')
                print(f"[{tries}] Retrying......   ", end='\r\r')
                sleep(2)
            except Exception as e:
                print("[-] Error Occured As : {e} ")
                self.EXIT_GRACEFULLY([self.SOCKET],-2)
        print(f"[+] Connected To {self.IP}:{self.PORT}")

    def accept(self):
        self.listen()
        self.CLIENT_CONN,self.CLIENT_ADDR=self.SOCKET.accept()
        print(f"[+] Received Connection From {self.CLIENT_ADDR[0]}:{self.CLIENT_ADDR[1]} ")

    def GENERATE_SESSION_KEY(self):
        self.SESSION_KEY=Fernet.generate_key()

    def SEND_PUBLIC_KEY(self,sock,tries):
        flag=False
        for i in range(0,tries):
            sock.send(self.PUBLIC_KEY.exportKey())
            TRIAL_HASH=sock.recv(1024).decode()
            if TRIAL_HASH==self.PUBLIC_KEY_HASH :
                sock.send('OK'.encode())
                print("[+] Sent Public Key !")
                flag=True
                break
            else :
                sock.send('ERROR'.encode())
        if not flag :
            print("[-] Failed To Send Public Key ")
            self.EXIT_GRACEFULLY([self.CLIENT_CONN,self.SOCKET],-3)
            
    def RECEIVE_PUBLIC_KEY(self,sock,tries):
        flag=False
        for i in range(0,tries):
            SERVER_KEY=sock.recv(1024)
            #print(SERVER_KEY.decode())
            TRIAL_HASH=md5(SERVER_KEY).hexdigest()
            sock.send(TRIAL_HASH.encode())
            CHECK=sock.recv(1024).decode()
            if CHECK[:2]=='OK':
                flag=True
                self.CLIENT_PUBLIC_KEY=SERVER_KEY
                self.ENCRYPTOR=RSA.importKey(SERVER_KEY)
                print(f"[+] Received Public Key !\n[+] Checks Passed !")
                break
        if not flag :
            print("[-] Failed To Receive Public Key ")
            self.EXIT_GRACEFULLY([self.CLIENT_CONN,self.SOCKET],-4)

    def ASYM_ENC(self,message):
        encryptor = PKCS1_OAEP.new(self.ENCRYPTOR)
        encrypted = encryptor.encrypt(message)
        return encrypted

    def SEND_ASYM_DATA(self,sock,message):
        sock.send(self.ASYM_ENC(message))

    def ASYM_DEC(self,message):
        decryptor = PKCS1_OAEP.new(self.KEYPAIR)
        decrypted = decryptor.decrypt(message)
        return(decrypted)
        
    def RECV_ASYM_DATA(self,sock,size=2048):
        return self.ASYM_DEC(sock.recv(size))

    def VALIDATE_CLIENT(self,sock,tries=3):
        data=self.NAME+"::"+self.HASH+"::"+secrets.token_urlsafe()
        self.SEND_ASYM_DATA(sock,data.encode())
        recv=self.RECV_ASYM_DATA(sock)
        if (recv).decode()=="NOTOK":
            return False
        else :
            self.SESSION_KEY=recv
            return True

    def VERIFY_CLIENT(self,sock,tries=3):
        data=self.RECV_ASYM_DATA(sock).decode().split("::")
        print(f"[+] Validating Credentials From {data[0]}::{self.CLIENT_ADDR[0]}")
        if data[1]==self.HASH :
            self.GENERATE_SESSION_KEY()
            self.SEND_ASYM_DATA(sock,self.SESSION_KEY)
            self.CLIENT_USERNAME=data[0]
            return True
        else :
            self.SEND_ASYM_DATA(sock,b"NOTOK")
            #self.EXIT_GRACEFULLY([self.SOCKET,self.CLIENT_CONN])
            return False

    def INIT_SESSION_ENCRYPTOR(self):
        self.GEN_SESSION_ENCRYPTOR=Fernet(self.SESSION_KEY)

    def EXIT_GRACEFULLY(self,SOCKS,CODE=-1):
        for sock in SOCKS :
            if sock != None :
                sock.close()
        exit(CODE)

