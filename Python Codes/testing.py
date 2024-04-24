from pynput.keyboard import Controller, Key
key_combination = ["a", "b"]
key_flag = False

keyboard = Controller()
# arrow_keys = itertools.cycle([Key.left, Key.right])

def press_arrow_key():
    global key_flag
    keyboard.press(key_combination[key_flag])
    keyboard.release(key_combination[key_flag])
    key_flag = not key_flag

try:
    while True:
        a = input("User input 1 or 0")
        press_arrow_key()
        

except:
    pass
finally:
    print("Done")