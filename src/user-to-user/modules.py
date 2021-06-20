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
        try :
            recv_msg=socket.recv(2048)
            if not recv_msg :
                sys.exit(0)
            recv_mess=DEC_MESS(cryptor,(recv_msg)).decode()
            print(f"{ip}:{name} ↴\n{recv_mess}\nYour Turn ↴")
        except :
            break

def SEND_DATA(socket,cryptor):
    while True:
        try :
            send_msg=input(str("Your Turn ↴ \n"))
            socket.send(ENC_MESS(cryptor,send_msg.encode()))
        except :
            break
