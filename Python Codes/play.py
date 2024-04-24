from pynput.keyboard import Controller, Key
import itertools

keyboard = Controller()
# arrow_keys = itertools.cycle([Key.left, Key.right])
arrow_keys = itertools.cycle(['a', 'b'])

def press_arrow_key():
    global arrow_keys
    keyboard.press(next(arrow_keys))
    keyboard.release(next(arrow_keys))