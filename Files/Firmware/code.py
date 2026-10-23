print("Starting")

import board
import touchio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.rgb import RGB
from kmk.extensions.rgb import AnimationModes
from kmk.extensions.media_keys import MIDI
from kmk.extensions import Extension

keyboard = KMKKeyboard()

COL1 = board.IO8
COL2 = board.IO9
COL3 = board.IO10
ROW1 = board.IO11
ROW2 = board.IO12
ENC_A = board.RX
ENC_B = board.TX
LED = board.IO13

TOUCH_PINS = [
    board.IO1, 
    board.IO2, 
    board.IO3, 
    board.IO4, 
    board.IO5, 
    board.IO6, 
    board.IO7, 
]

TOUCH_NOTES = [60, 62, 64, 65, 67, 69, 71]

class CapacitiveTouchMidi(Extension):
    def __init__(self, pins, notes):
        self.touch_pads = [touchio.TouchIn(pin) for pin in pins]
        self.notes = notes
        self.pad_states = [False] * len(pins)

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        return

    def before_matrix_scan(self, sandbox):
        for i, pad in enumerate(self.touch_pads):
            is_touched = pad.value
            if is_touched and not self.pad_states[i]:
                sandbox.extensions.MIDI.send_note_on(self.notes[i], 127)
                self.pad_states[i] = True
            elif not is_touched and self.pad_states[i]:
                sandbox.extensions.MIDI.send_note_off(self.notes[i], 0)
                self.pad_states[i] = False

    def after_matrix_scan(self, sandbox):
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

touch_midi_ext = CapacitiveTouchMidi(TOUCH_PINS, TOUCH_NOTES)
keyboard.extensions.append(touch_midi_ext)

keyboard.col_pins = (COL1,COL2,COL3)
keyboard.row_pins = (ROW1,ROW2)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.keymaps = [
    [KC.ESC, KC.DELETE, KC.PSCREEN,
     KC.LEFT, KC.PAUSE, KC.RIGHT,
    ]
]

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)
encoder_handler.pins = ((ENC_A, ENC_B, None, False),)
encoder_handler.map = (((KC.VOLD, KC.VOLU),),)

rgb_ext = RGB(
    pixel_pin = LED,
    num_pixels = 6,
    val_limit = 100,
    val_default = 75,
    animation_speed = 1,
    animation_mode = AnimationModes.KNIGHT,
    refresh_rate = 50,
)
keyboard.extensions.append(rgb_ext)

midi = MIDI()
keyboard.extensions.append(midi)

if __name__ == '__main__':
    keyboard.go()