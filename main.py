from pynput.keyboard import Key, Listener
from pynput import mouse
from colorama import init, Fore, Back, Style
from time import sleep
import threading
import random
import pygame
import json
import os

init()

pressedKeys = []
folders = []
mousefolders = []

pygame.mixer.init()
os.system("cls")

with open("config.json", "r", encoding='utf-8') as config_file:
    data = json.load(config_file)

volume = data['volume']
folder = data['folder']
mousefolder = data['mousefolder']
mouseSounds = data['mousesounds']

os.system(f"title MechaVibes ｜ {folder} ｜ {mousefolder} ｜ Volume: {str(volume)}")

with open(f"soundpacks/{folder}/pack_config.json", "r", encoding='utf-8') as pack_config:
    pack_data = json.load(pack_config)

with open(f"mousepacks/{mousefolder}/pack_config.json", "r", encoding='utf-8') as mousepack_config:
    mousepack_data = json.load(mousepack_config)

def resetPlayer():
    while True:
        sleep(60*2)
        pygame.mixer.quit()
        pygame.mixer.init()

def commandlistener():
    while True:
        global volume
        global folder
        global pack_data
        global mouseSounds
        global mousefolder
        global mousefolders
        global mousepack_data

        mouseSounds = data['mousesounds']

        print(f"""
                            
                    {Fore.LIGHTCYAN_EX}███╗   ███╗███████╗ ██████╗██╗  ██╗ █████╗ ██╗   ██╗██╗██████╗ ███████╗███████╗
                    ████╗ ████║██╔════╝██╔════╝██║  ██║██╔══██╗██║   ██║██║██╔══██╗██╔════╝██╔════╝
                    ██╔████╔██║█████╗  ██║[1.0]███████║███████║██║   ██║██║██████╔╝█████╗  ███████╗
                    ██║╚██╔╝██║██╔══╝  ██║     ██╔══██║██╔══██║╚██╗ ██╔╝██║██╔══██╗██╔══╝  ╚════██║
                    ██║ ╚═╝ ██║███████╗╚██████╗██║  ██║██║  ██║ ╚████╔╝ ██║██████╔╝███████╗███████║
                    ╚═╝     ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚═════╝ ╚══════╝╚══════╝{Fore.RESET}
                
                                                                                            
[Current keyboard soundpack]: {Fore.LIGHTCYAN_EX}{folder}{Fore.RESET} 
[Current mouse soundpack]: {Fore.LIGHTCYAN_EX}{mousefolder}{Fore.RESET} 
[Mouse sounds]: {Fore.LIGHTCYAN_EX}{str(mouseSounds)}{Fore.RESET} 
[Volume]: {Fore.LIGHTCYAN_EX}{volume}{Fore.RESET} 
""")
        command = input("\nEnter command: ")

        if "volume" in command:
            try:
                data['volume'] = float(command.split(" ")[1])
                volume = float(command.split(" ")[1])

                with open("config.json", "w") as config_file:
                    json.dump(data, config_file)

                os.system(f"title MechaVibes ｜ {folder} ｜ {mousefolder} ｜ Volume: {str(volume)}")

            except:
                print("Wrong command usage.")
                sleep(1)
                os.system("cls")
        
        if "folder" in command:
            try:
                choice = input(f"{Fore.LIGHTCYAN_EX}Keyboard{Fore.RESET} / {Fore.LIGHTCYAN_EX}Mouse{Fore.RESET}: ")
                if choice == "keyboard":
                    
                    for item in next(os.walk('soundpacks'))[1]:
                        if item not in folders:
                            folders.append(''.join(item))

                    print("\n==========| Folders |==========\n")
                    for item in folders:
                        indexOfItem = folders.index(item)
                        print(str(indexOfItem) + ": " + Fore.LIGHTCYAN_EX + item + Fore.RESET)

                    folderName = int(input("\nEnter folder number: "))

                    data['folder'] = folders[folderName]
                    folder = folders[folderName]

                    with open(f"soundpacks/{folder}/pack_config.json", "r", encoding='utf-8') as pack_config:
                        pack_data = json.load(pack_config)

                    with open("config.json", "w") as config_file:
                        json.dump(data, config_file)

                    os.system(f"title MechaVibes ｜ {folder} ｜ {mousefolder} ｜ Volume: {str(volume)}")

                
                elif choice == "mouse":
                    for item in next(os.walk('mousepacks'))[1]:
                        if item not in mousefolders:
                            mousefolders.append(''.join(item))

                    print("\n==========| Folders |==========\n")
                    for item in mousefolders:
                        indexOfItem = mousefolders.index(item)
                        print(str(indexOfItem) + ": " + Fore.LIGHTCYAN_EX + item + Fore.RESET)

                    folderName = int(input("\nEnter folder number: "))

                    data['mousefolder'] = mousefolders[folderName]
                    mousefolder = mousefolders[folderName]

                    with open(f"mousepacks/{mousefolder}/pack_config.json", "r", encoding='utf-8') as mousepack_config:
                        mousepack_data = json.load(mousepack_config)

                    with open("config.json", "w") as config_file:
                        json.dump(data, config_file)

                    os.system(f"title MechaVibes ｜ {folder} ｜ {mousefolder} ｜ Volume: {str(volume)}")

            except Exception as e:
                print(f"Wrong command usage. {e}")
                sleep(1)
                os.system("cls")

        if "mouse" in command:
            if mouseSounds != True:
                mouseSounds = True
                data['mousesounds'] = True
            else:
                mouseSounds = False
                data['mousesounds'] = False

            with open("config.json", "w") as config_file:
                json.dump(data, config_file)

        os.system("cls")

def on_press(key):
    if key not in pressedKeys:
        try:
            pressedKeys.append(key)
            mp3file = pack_data[str(key).lower().replace("'", "")]
            sound = pygame.mixer.Sound(f"soundpacks/{folder}/{mp3file}")
            sound.set_volume(volume)
            sound.play()
        except:
            sound = pygame.mixer.Sound(f"soundpacks/{folder}/{str(random.randint(1, 2))}.mp3")
            sound.set_volume(volume)
            sound.play()

def on_release(key):
    if key in pressedKeys:
        pressedKeys.remove(key)
    # i did sum fix here

def on_click(x, y, button, pressed):
    if pressed and mouseSounds:
        try:
            pressedKeys.append(button)
            mp3file = mousepack_data[str(button).lower().replace("'", "")]
            sound = pygame.mixer.Sound(f"mousepacks/{mousefolder}/{mp3file}")
            sound.set_volume(volume)
            sound.play()
        except:
            sound = pygame.mixer.Sound(f"mousepacks/{mousefolder}/{str(random.randint(1, 2))}.mp3")
            sound.set_volume(volume)
            sound.play()

my_thread = threading.Thread(target=commandlistener)
reset_player_thread = threading.Thread(target=resetPlayer)

my_thread.start()
reset_player_thread.start()

listener = mouse.Listener(on_click=on_click)
listener.start()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
