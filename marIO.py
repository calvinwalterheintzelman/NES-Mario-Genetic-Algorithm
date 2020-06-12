import pyautogui
import time
import ctypes
import numpy as np
import copy

pix_x = 75
pix_y = 116
pix_len = pix_x * pix_y
button_press_value = 4210000
individuals = 100
survivors = 10
layer1_len = 20
layer2_len = 16
output_len = 12
mutation_rate = 0.08

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


def get_weights(next_nodes, prev_nodes):
    return [np.random.uniform(-1, 1, prev_nodes) for q in range(next_nodes)]


# initialize first layer (input)
population = [get_weights(layer1_len, pix_len) for i in range(individuals)]

# add a 20 layer and 16 layer of weights
weights1 = [get_weights(layer2_len, layer1_len) for j in range(individuals)]
weights2 = [get_weights(output_len, layer2_len) for k in range(individuals)]

# add a bias term for population, 20 weight layer, and 16 weight layer
pop_bias = [np.random.uniform(-100, 100, layer1_len) for l in range(individuals)]
wt1_bias = [np.random.uniform(-100, 100, layer2_len) for m in range(individuals)]
wt2_bias = [np.random.uniform(-100, 100, output_len) for n in range(individuals)]

generation = 0

'''
 pixel vales can be one of the following:
1. 545
2. 232
3. 657
4. 0
5. 762
6. 
7. 
8. 
9. 
10. 
11. 
12. 
'''

while True:
    max_index = [i for i in range(survivors)]
    max_score = [-1 for i in range(survivors)]
    for m in range(individuals):
        rjump()
        rrun()
        rup()
        rdown()
        rright()
        rleft()
        not_dead = True
        score = 0
        time_since_change = time.time()
        old_pixel = 0
        PressKey(59)
        ReleaseKey(59)
        time.sleep(1)
        while not_dead:
            check1 = time.perf_counter()
            # Statement below is correct when set to x1 in top left corner in NES emulator
            screen = pyautogui.screenshot(region=(1, 100, 293, 193))
            screen = screen.resize(size=(pix_y, pix_x))
            screen.save('/Users/butt/PycharmProjects/MarIO_Project/Screen.png')
            pixels = [sum(x) for x in np.array(screen.getdata())]

            '''
            # used for testing possible pixel values
            types = []
            for asdf in pixels:
                if sum(asdf) not in types:
                    types.append(sum(asdf))
            print(types)
            '''

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
            layer1 = [population[m][z].dot(pixels) + pop_bias[m][z] for z in range(layer1_len)]
            layer2 = [weights1[m][z].dot(layer1) + wt1_bias[m][z] for z in range(layer2_len)]
            output = [weights2[m][z].dot(layer2) + wt2_bias[m][z] for z in range(output_len)]

            while time.perf_counter() - check1 < 0.3:
                pass

            # 1)
            if output[0] > 0:
                hjump()
            if output[1] > 0:
                rjump()
            # 2
            if output[2] > 0:
                hrun()
            if output[3] > 0:
                rrun()
            # 3
            if output[4] > 0:
                hright()
            if output[5] > 0:
                rright()
            # 4
            if output[6] > 0:
                hleft()
            if output[7] > 0:
                rleft()
            # 5
            if output[8] > 0:
                hup()
            if output[9] > 0:
                rup()
            # 6
            if output[10] > 0:
                hdown()
            if output[11] > 0:
                rdown()

            # to assure precise timing
            while time.perf_counter() - check1 < 0.33:
                pass

        for i in range(len(max_score)):
            if score > max_score[i] == min(max_score):
                max_score[i] = score
                # print("Max index is: " + str(m))
                # print("Score is: " + str(score))
                max_index[i] = copy.deepcopy(m)
                break
        print("Individual " + str(m) + " dead; score below")
        print(max_score)
        print(max_index)

    # population reproduction and mutations
    temp = [copy.deepcopy(population[max_index[i]]) for i in range(survivors)]
    for i in range(survivors):
        population[i] = copy.deepcopy(temp[i])
    for i in range(survivors):
        for j in range((individuals - survivors) // survivors):
            population[i + (j + 1) * survivors] = copy.deepcopy(population[j])
    for i in range(individuals - survivors):
        for j in range(layer1_len):
            for k in range(pix_len):
                if np.random.rand() < mutation_rate:
                    population[i + survivors][j][k] = np.random.uniform(-1, 1)

    # weights1 reproduction and mutations
    temp = [copy.deepcopy(weights1[max_index[i]]) for i in range(survivors)]
    for i in range(survivors):
        weights1[i] = copy.deepcopy(temp[i])
    for i in range(survivors):
        for j in range((individuals - survivors) // survivors):
            weights1[i + (j + 1) * survivors] = copy.deepcopy(weights1[j])
    for i in range(individuals - survivors):
        for j in range(layer2_len):
            for k in range(layer1_len):
                if np.random.rand() < mutation_rate:
                    weights1[i + survivors][j][k] = np.random.uniform(-1, 1)

    # weights2 reproduction and mutations
    temp = [copy.deepcopy(weights2[max_index[i]]) for i in range(survivors)]
    for i in range(survivors):
        weights2[i] = copy.deepcopy(temp[i])
    for i in range(survivors):
        for j in range((individuals - survivors) // survivors):
            weights2[i + (j + 1) * survivors] = copy.deepcopy(weights2[j])
    for i in range(individuals - survivors):
        for j in range(output_len):
            for k in range(layer2_len):
                if np.random.rand() < mutation_rate:
                    weights2[i + survivors][j][k] = np.random.uniform(-1, 1)

    # bias reproduction and mutations
    # population bias
    temp = [copy.deepcopy(pop_bias[max_index[i]]) for i in range(survivors)]
    for i in range(survivors):
        pop_bias[i] = copy.deepcopy(temp[i])
    for i in range(survivors):
        for j in range((individuals - survivors) // survivors):
            pop_bias[i + (j + 1) * survivors] = copy.deepcopy(pop_bias[j])
    for i in range(individuals - survivors):
        for j in range(layer1_len):
            if np.random.rand() < mutation_rate:
                pop_bias[i + survivors][j] = np.random.uniform(-100, 100)

    # weights1 bias
    temp = [copy.deepcopy(wt1_bias[max_index[i]]) for i in range(survivors)]
    for i in range(survivors):
        wt1_bias[i] = copy.deepcopy(temp[i])
    for i in range(survivors):
        for j in range((individuals - survivors) // survivors):
            wt1_bias[i + (j + 1) * survivors] = copy.deepcopy(wt1_bias[j])
    for i in range(individuals - survivors):
        for j in range(layer2_len):
            if np.random.rand() < mutation_rate:
                wt1_bias[i + survivors][j] = np.random.uniform(-100, 100)

    # weights2 bias
    temp = [copy.deepcopy(wt2_bias[max_index[i]]) for i in range(survivors)]
    for i in range(survivors):
        wt2_bias[i] = copy.deepcopy(temp[i])
    for i in range(survivors):
        for j in range((individuals - survivors) // survivors):
            wt2_bias[i + (j + 1) * survivors] = copy.deepcopy(wt2_bias[j])
    for i in range(individuals - survivors):
        for j in range(output_len):
            if np.random.rand() < mutation_rate:
                wt2_bias[i + survivors][j] = np.random.uniform(-100, 100)

    '''
    fp = open("Pop.txt", 'w')
    for array in population[0]:zzjizjizji
        for num in array:
            fp.write(str(num) + '\n')
        fp.write("done\n")
    fp.write("DONE\n")
    fp.close()
    '''

    print()
    print("Generation " + str(generation))
    generation += 1
    print("Average max score is: " + str(sum(max_score) / len(max_score)))
    print()


# print(pixels[len(pixels)-1])
# print(old_pixel)
# print(tuple(old_pixel) == tuple(pixels[len(pixels)-1]))
# this all works (the print statements)

# The network will get points every time the bottom right pixel changes
