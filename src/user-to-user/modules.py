from colorama import init, Fore, Back, Style
from cryptography.fernet import Fernet
import sys

def showMyInfo(username,ip,port):
    init(autoreset=True)
    print(f"\n[+] Username     : {Style.BRIGHT + Back.CYAN + Fore.WHITE + username}")
    print(f"[+] Listening On : {Style.BRIGHT + Back.BLUE + Fore.WHITE + ip+':'+str(port)}")
    print(f"[+] Password     : {Style.BRIGHT + Back.MAGENTA + Fore.WHITE + '*'*12}")
    print(Style.RESET_ALL)

def ENC_MESS(cryptor,message):
    return cryptor.encrypt(message)

def DEC_MESS(cryptor,message):
    return cryptor.decrypt(message)

def RECV_DATA(socket,cryptor,ip,name="Sender"):        
    while True:
        recv_msg=socket.recv(2048)
        if not recv_msg :
            sys.exit(0)
        recv_mess=DEC_MESS(cryptor,(recv_msg)).decode()
        print(f"\n{ip}:{name} > {recv_mess}")

def SEND_DATA(socket,cryptor):
    while True:
        send_msg=input(str("\nMe > "))
        socket.send(ENC_MESS(cryptor,send_msg.encode()))
