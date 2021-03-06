#!/usr/bin/env python3
import threading
import sys
import argparse
import getpass
from hashlib import sha256
from Encryption import *
from modules import *

def main():
    print("[+] End-2-End Encrypted Chatroom By @whokilleddb")
    
    #Parse Command Line Arguments
    parser = argparse.ArgumentParser(description="[+] End To End Encrypted Chat Room By : @whokilleddb")
    parser.add_argument('-i', metavar='IP to connect to', required=True, help="IP to connect to")
    parser.add_argument('-p', metavar='Port to connect to', required=False,default=8080, type=int, help="Port connect to")
    parser.add_argument('-n', metavar='Username', required=False,default="Client", type=str, help="Username for the session")
    args = parser.parse_args()

    #Get Passwd
    passwd=getpass.getpass(prompt=f'[+] Enter Room Password : ', stream=None)
    passhash=sha256(passwd.encode()).hexdigest()
    #print(passhash)

    #Print Info
    showMyInfo(args.n,args.i,args.p)
    
    #Generate User
    print("[+] Generating Session Profile")
    myuser=User(args.n,args.i,args.p,passhash)
   
    #Connect To A Port
    myuser.connect()
    myuser.RECEIVE_PUBLIC_KEY(myuser.SOCKET,3)
    myuser.SEND_PUBLIC_KEY(myuser.SOCKET,3)

    if not myuser.VALIDATE_CLIENT(myuser.SOCKET) :
        print("[-] Verification Attempt Failed")
        myuser.EXIT_GRACEFULLY([myuser.SOCKET])
    else :
        print("[+] Successfully Verified Client")
#       print(f"[+] Session Key : \n {myuser.SESSION_KEY}")  
        myuser.INIT_SESSION_ENCRYPTOR()      
#       print(myuser.SESSION_KEY)
        print("[+] Starting Session : ")

        try :
            t = threading.Thread(target=RECV_DATA,args=(myuser.SOCKET,myuser.GEN_SESSION_ENCRYPTOR,args.i,"Server"))
            t.start()
            SEND_DATA(myuser.SOCKET,myuser.GEN_SESSION_ENCRYPTOR)
        except Exception as e : 
            print("[-] Got Exception As {e}\n[-] Exiting!")
            myuser.EXIT_GRACEFULLY([myuser.SOCKET])

if __name__ == '__main__' :
    main()
