from colorama import init, Fore, Back, Style

def showMyInfo(username,ip,port,passhash):
    init(autoreset=True)
    print(f"\n[+] Username     : {Style.BRIGHT + Back.CYAN + Fore.WHITE + username}")
    print(f"[+] Listening On : {Style.BRIGHT + Back.BLUE + Fore.WHITE + ip+':'+str(port)}")
    print(f"[+] Password     : {Style.BRIGHT + Back.MAGENTA + Fore.WHITE + '*'*12}")
    print(Style.RESET_ALL)
