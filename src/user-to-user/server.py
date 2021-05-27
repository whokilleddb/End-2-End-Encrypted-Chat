#!/usr/bin/env python3
import sys
import argparse
import getpass
from hashlib import sha256
from Encryption import *
from modules import *

def main() :
    print("[+] End-2-End Encrypted Chatroom By @whokilleddb")
    #Parse Command Line Arguments
    parser = argparse.ArgumentParser(description="[+] End To End Encrypted Chat Room By : @whokilleddb")
    parser.add_argument('-i', metavar='IP to listen on', required=False,default="0.0.0.0", type=str, help="IP to Listen On")
    parser.add_argument('-p', metavar='Port to bind', required=False,default=8080, type=int, help="Port to bind to")
    parser.add_argument('-n', metavar='Username', required=False,default="Server", type=str, help="Username for the session")
    args = parser.parse_args()

    #Get Passwd
    passwd=getpass.getpass(prompt=f'[+] Set Password For This Session : ', stream=None)
    passhash=sha256(passwd.encode()).hexdigest()
    #print(passhash)

    #Print Info
    showMyInfo(args.n,args.i,args.p,passhash)
    
    #Generate User
    print("[+] Generating Session Profile")
    myuser=User(args.n,args.i,args.p,passhash)
    print(f"[+] Your Public Key : \n{myuser.PUBLIC_KEY.exportKey().decode()}\n[+] MD5Sum : {myuser.PUBLIC_KEY_HASH}")

    #Listen On A Port
    myuser.accept()
    myuser.SEND_PUBLIC_KEY(myuser.CLIENT_CONN,3)

if __name__ == '__main__' :
    main()