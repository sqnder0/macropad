import board
import busio
import digitalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import KeysScanner
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306

keyboard = KMKKeyboard()

keyboard.matrix = KeysScanner(
    pins=[board.D10, board.D9, board.D8, board.D7, board.D6, board.D3],
    value_when_pressed=False,
    pull=digitalio.Pull.UP,
)

keyboard.keymap = [[
    KC.VOLU, KC.MUTE, KC.VOLD,
    KC.MPRV, KC.MPLY, KC.MNXT,
]]

encoder = EncoderHandler()
keyboard.modules.append(encoder)
encoder.pins = ((board.D0, board.D1, board.D2, False),)
encoder.map = [((KC.VOLD, KC.VOLU, KC.MUTE),)]

i2c_bus = busio.I2C(board.D5, board.D4)
driver = SSD1306(i2c=i2c_bus, device_address=0x3C)
display = Display(
    display=driver,
    entries=[TextEntry(text="Soundpad", x=0, y=0)],
    width=128,
    height=32,
    dim_time=10,
    dim_target=0.1,
    off_time=1200,
    brightness=0.8,
)
keyboard.extensions.append(display)

if __name__ == "__main__":
    keyboard.go()