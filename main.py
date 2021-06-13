import os  
import sys
import shutil
import time as t
import pathlib
import time
from colored import fg, bg, attr
import pyttsx3
from datetime import date
from datetime import time
from datetime import datetime
import subprocess
import difflib
from difflib import SequenceMatcher, get_close_matches, Differ
from pprint import pprint
import re
import win32con
import win32api
import winreg as reg
from playsound import playsound
import plyer
import itertools
import threading
from plyer import notification
import win32ui
import win32con
import ctypes
import enum
import getpass
import sys
import admin
import traceback
import types
from subprocess import call
import win32api
import win32con
import win32event
import win32process
from win32com.shell.shell import ShellExecuteEx
from win32com.shell import shellcon
import logging
import math
import winreg as reg

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if is_admin():
    # Code of your program here
    pass
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


def tempDeleter():
    changeCWD = os.chdir("C:\\Users\\USER\\AppData\\Local\\Temp")
    items = os.listdir()
    for i in items:
        try:
            os.remove(i)
            print(f"{fg('green_1')}Removed {i}{attr('reset')}")
        except Exception:
            print("Item in use")








if __name__ == '__main__':
    tempDeleter()


