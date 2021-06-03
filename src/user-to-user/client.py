#!/usr/bin/env python3
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
    showMyInfo(args.n,args.i,args.p,passhash)
    
    #Generate User
    print("[+] Generating Session Profile")
    myuser=User(args.n,args.i,args.p,passhash)
    print(f"[+] Your Public Key : \n{myuser.PUBLIC_KEY.exportKey().decode()}\n[+] MD5Sum : {myuser.PUBLIC_KEY_HASH}")

    #Connect To A Port
    myuser.connect()
    myuser.RECEIVE_PUBLIC_KEY(myuser.SOCKET,3)
    myuser.SEND_PUBLIC_KEY(myuser.SOCKET,3)
    if not myuser.VALIDATE_CLIENT(myuser.SOCKET) :
        print("[-] Verification Attempt Failed")
        myuser.EXIT_GRACEFULLY([myuser.SOCKET])
    else :
        print("[+] Successfully Verified Client")
        print(f"[+] Session Key : \n {myuser.SESSION_KEY}")        

    

if __name__ == '__main__' :
    main()