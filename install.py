from sshkeyboard import listen_keyboard
from colorama import Cursor, Fore
from colorama import Back
from colorama.initialise import init
from enum import Enum
from functools import partial
import os

### Constants ###
INFO = "./info"
DATA = "./data"
LOGO = Fore.BLACK + """   ___
 _| """ + Fore.YELLOW + "_" + Fore.BLACK + """ |_
|  """ + Fore.YELLOW + "/ \\" + Fore.BLACK + """  |
|_""" + Fore.YELLOW + " \\_/" + Fore.BLACK + """ _|
  |___| """
VERSION = "1.0"


class PlatformSupport(Enum):
    WINDOWS = 1
    LINUX = 2
    BOTH = 3

class Menu():
    def __init__(self, options: list) -> None:

        self.options = options
        self.selection = self.options[0]
        self.__cursor_pos = len(self.options) - 1

        for s in options:
            print(f"\t{s}")
            self.__cursor_pos -= 1 
        print(Cursor.UP(), end="")
        self.__cursor_pos += 1
        listen_keyboard(on_press=self.__on_press, until="enter", delay_other_chars=0.01, delay_second_char=0.01) 
        print(Cursor.DOWN(len(options) - 1))


    def __on_press(self, key) -> None:
        if key == "up":
            self.__hover(1)
        elif key == "down":
            self.__hover(-1)

    def __on_select(self, option) -> str:
        return Fore.YELLOW + f"\t  > {option}" + Fore.RESET

    def __hover(self, move: int) -> None:
        
        print("\033[2K\033[G", end="")
        print(Fore.RESET + "\t" + self.selection, end="\r")

        self.selection = self.options[((self.options.index(self.selection) + move) + len(self.options)) % len(self.options)]

        if self.__cursor_pos == len(self.options) - 1 and move > 0:
            print(Cursor.DOWN(len(self.options) - 2))
            self.__cursor_pos = 0
        elif self.__cursor_pos == 0 and move < 0:
            print(Cursor.UP(len(self.options)))
            self.__cursor_pos = len(self.options) - 1
        else:
            if move < 0:
                print(Cursor.DOWN(abs(move)), end = "")
                self.__cursor_pos -= 1
            else:
                print(Cursor.UP(abs(move)), end = "")
                self.__cursor_pos += 1
    
        print("\033[2K\033[G", end="")
        print(self.__on_select(self.selection), end="\r")

class Configuration():
    def __init__(self, id: str, platform: PlatformSupport, conf_version: int) -> None:
        self.id = id
        self.platform = platform
        self.conf_version = conf_version
        self.__validate_folder_structure()


    def __validate_folder_structure(self) -> None:
        if self.platform == PlatformSupport.WINDOWS or self.platform == PlatformSupport.BOTH:
            if not os.path.exists(INFO + "/" + self.id + "/win.bat"):
                raise Exception("Windos install script missing!")

        if self.platform == PlatformSupport.LINUX or self.platform == PlatformSupport.LINUX:
            if not os.path.exists(INFO + "/" + self.id + "/linux.sh"):
                raise Exception("Linux install script missing!")

        if not os.path.exists(DATA + "/" + self.id):
            raise Exception("Data entry missing!")

def main():
    init()

    print(LOGO, end = " ")
    print(Fore.YELLOW + "conf-everything " + Fore.BLACK + Back.YELLOW + "v" + VERSION + Fore.RESET + Back.RESET)

    menu = Menu([
        "Test1",
        "Test2",
        "Test3"
        ])
    
    print(menu.selection)

if __name__ == '__main__':
    main()
