# next steps: try out serenade on linux, and try the press thing on linux as well (if # works), figure out if the keyboard is plug and play

import pyautogui as pg
import pyperclip
import time

# communicate with arduino via usb
import serial
s = serial.Serial(port='COM4')


# timers
MIN_TIME_BETWEEN_PRESSES = 0.05
MIN_AFTER_UNPRESS = 0.05


# keys initialization
class Key:
    def __init__(self, default, shift=None, symbol1=None, symbol2=None):
        self.default = default
        self.shift = shift
        self.symbol1 = symbol1
        self.symbol2 = symbol2
        self.last_press_time = 0 # in seconds since 1970
        self.last_unpress = 0
    
    def press(self, modifier_string):
        is_shift = modifier_string[0] == "Y"
        is_sym1 = modifier_string[1] == "Y"
        is_sym2 = modifier_string[2] == "Y"
        is_control = modifier_string[3] == "Y"
        is_alt = modifier_string[4] == "Y"
        
        # get currently pressed key (aka which character)
        current_key = self.default
        if is_sym2 and self.symbol2 != None:
            current_key = self.symbol2
        if is_sym1 and self.symbol1 != None:
            current_key = self.symbol1
        if is_shift and self.shift != None:
            current_key = self.shift
        
        # check both timers
        if time.time() - self.last_press_time < MIN_TIME_BETWEEN_PRESSES: 
            return
        elif time.time() - self.last_unpress < MIN_AFTER_UNPRESS:
            return
        else:
            # later differentiate between hot key and normal press
            if is_control:
                pg.hotkey('ctrl', current_key)
            elif is_alt:
                pg.hotkey('alt', current_key)
            # some symbols have to be pasted in because their position differs on keyboards
            elif current_key in special_symbols:
                old = pyperclip.paste()
                pyperclip.copy(current_key)
                pg.hotkey('ctrl', 'v')
                pyperclip.copy(old)
            else:
                pg.press(current_key)
            # reset timer
            self.last_press_time = time.time()
                
        
    def un_press(self):
        self.last_unpress = time.time()



    
# ----
# initialize all the different keys
# ----
keys = [None for i in range(55)]
keys[1] = Key('winleft')
keys[4] = Key('space')
keys[7] = Key(',', ';')
keys[8] = Key('.', ':')
keys[9] = Key('-', '_')
keys[10] = Key('backspace')
# key 11 is shift
keys[12] = Key('<', '>')
keys[13] = Key('z', 'Z')
keys[14] = Key('x', 'X')
keys[15] = Key('c', 'C')
keys[16] = Key('v', 'V')
keys[17] = Key('b', 'B')
keys[18] = Key('n', 'N')
keys[19] = Key('m', 'M')
# key 21 is shift
keys[23] = Key('a', 'A')
keys[24] = Key('s', 'S')
keys[25] = Key('d', 'D')
keys[26] = Key('f', 'F')
keys[27] = Key('g', 'G')
keys[28] = Key('h', 'H')
keys[29] = Key('j', 'J')
keys[30] = Key('k', 'K', '{', '`') # missing spanish ~?
keys[31] = Key('l', 'L', '}')
keys[32] = Key('enter')
keys[33] = Key('tab', '\\')
keys[34] = Key('q', 'Q')
keys[35] = Key('w', 'W')
keys[36] = Key('e', 'E')
keys[37] = Key('r', 'R')
keys[38] = Key('t', 'T')
keys[39] = Key('y', 'Y')
keys[40] = Key('u', 'U')
keys[41] = Key('i', 'I', '[')
keys[42] = Key('o', 'O', ']')
keys[43] = Key('p', 'P', '+', '*')
keys[44] = Key('escape')
keys[45] = Key('1', '!', '|')
keys[46] = Key('2', '"', '@')
keys[47] = Key('3', '.', '#')
keys[48] = Key('4', '$', '~')
keys[49] = Key('5', '%')
keys[50] = Key('6', '&')
keys[51] = Key('7', '/')
keys[52] = Key('8', '(', '^')
keys[53] = Key('9', ')', '?', "'")
keys[54] = Key('0', '=') # missing symbols for spanish open? and!

special_symbols = ['\\', '!', '|', '#', '{', '}', "'", '=', '?', '/', '(', ')', '^', '%', '&', '$', '~', '"', '<', '>']


# ---
# receive usb inputs in a loop
# ---
while True:
    # read and pre-process usb output
    line = str(s.readline())
    while len(line) > 0 and line[0] != 'N' and line[0] != 'Y':
        line = line[1:]
    while len(line) > 0 and line[-1] != '/' and line[-1] != ',':
        line = line[:-1]
    split = line.split('/')

    # extract each list of keys
    mod_string = split[0]
    down_list = []
    up_list = []
    for key in split[1].split(','):
        if len(key) > 0:
            up_list.append(int(key))
    for key in split[2].split(','):
        if len(key) > 0:
            down_list.append(int(key))
            
    # tell each key in the up list to unpress
    for index in up_list:
        if keys[index] != None:
            keys[index].un_press()
    
    # tell each key in the down list to press
    for index in down_list:
        if keys[index] != None:
            keys[index].press(mod_string)
    
