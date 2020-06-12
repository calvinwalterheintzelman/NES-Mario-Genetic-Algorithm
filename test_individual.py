import pyautogui
import time
import ctypes
import numpy as np
import copy

pix_len = 56549
button_press_value = 4210000

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actual Functions
def PressKey(hexkeycode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexkeycode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexkeycode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexkeycode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


#  KEY PRESSES
def hjump():
    PressKey(0x2d)


def rjump():
    ReleaseKey(0x2d)


def hrun():
    PressKey(0x2c)


def rrun():
    ReleaseKey(0x2c)


def hright():
    PressKey(0x26)


def rright():
    ReleaseKey(0x26)


def hleft():
    PressKey(0x24)


def rleft():
    ReleaseKey(0x24)


def hup():
    PressKey(0x17)


def rup():
    ReleaseKey(0x17)


def hdown():
    PressKey(0x25)


def rdown():
    ReleaseKey(0x25)


score = 0
old_pixel = 0
not_dead = True
time_since_change = time.time()

population = []
fp = open("Pop.txt", 'r')
line = fp.readline()
while line != "DONE\n":
    arr_list = []
    while line != "done\n":
        arr_list.append(float(line))
        line = fp.readline()
    population.append(np.array(arr_list))
    line = fp.readline()

PressKey(59)
ReleaseKey(59)
time.sleep(0.5)
while not_dead:
    # Statement below is correct when set to x1 in top left corner in NES emulator
    screen = pyautogui.screenshot(region=(1, 100, 293, 193))
    screen = screen.convert('L')
    screen.save('/Users/butt/PycharmProjects/MarIO_Project/Screen.png')
    pixels = np.array(screen.getdata())
    # print(pixels)
    # print(len(pixels))
    new_pixel = pixels[len(pixels) - 1]
    if new_pixel != old_pixel:
        time_since_change = time.time()
        old_pixel = new_pixel
        # print("score!")
        score += 1
    time_curr = time.time()
    if time_curr - time_since_change > 5 or \
            (new_pixel == 0 and pixels[len(pixels) - 2] == 0 and pixels[len(pixels) - 3] == 0):
        not_dead = False

    # button presses/releases
    # 1
    if population[0].dot(pixels) > button_press_value:
        hjump()
    if population[1].dot(pixels) > button_press_value:
        rjump()
    # 2
    if population[2].dot(pixels) > button_press_value:
        hrun()
    if population[3].dot(pixels) > button_press_value:
        rrun()
    # 3
    if population[4].dot(pixels) > button_press_value:
        hright()
    if population[5].dot(pixels) > button_press_value:
        rright()
    # 4
    if population[6].dot(pixels) > button_press_value:
        hleft()
    if population[7].dot(pixels) > button_press_value:
        rleft()
    # 5
    if population[8].dot(pixels) > button_press_value:
        hup()
    if population[9].dot(pixels) > button_press_value:
        rup()
    # 6
    if population[10].dot(pixels) > button_press_value:
        hdown()
    if population[11].dot(pixels) > button_press_value:
        rdown()
    time.sleep(0.25)

rjump()
rrun()
rup()
rdown()
rright()
rleft()
