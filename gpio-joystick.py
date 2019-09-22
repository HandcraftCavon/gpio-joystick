import uinput
import RPi.GPIO as GPIO
import smbus

DPAD_UP = 1
DPAD_DOWN = 1
DPAD_LEFT = 1
DPAD_RIGHT = 1
A = 1
B = 1
X = 1
Y = 1
TL = 1
TR = 1
TL2 = 1
TR2 = 1
START = 1
SELECT = 1

joystick_left_x_channel = 1
joystick_left_y_channel = 2
joystick_right_x_channel = 3
joystick_right_y_channel = 4

joystick_left_x_reverse = False
joystick_left_y_reverse = False
joystick_right_x_reverse = False
joystick_right_y_reverse = False

joystick_left_x_last = -1
joystick_left_y_last = -1
joystick_right_x_last = -1
joystick_right_y_last = -1

events = (
    uinput.BTN_DPAD_UP,
    uinput.BTN_DPAD_DOWN,
    uinput.BTN_DPAD_LEFT,
    uinput.BTN_DPAD_RIGHT,
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_TL,
    uinput.BTN_TR,
    uinput.BTN_TL2,
    uinput.BTN_TR2,
    uinput.BTN_START,
    uinput.BTN_SELECT,
    uinput.ABS_X + (0, 255, 0, 0),
    uinput.ABS_Y + (0, 255, 0, 0),
    uinput.ABS_RX + (0, 255, 0, 0),
    uinput.ABS_RY + (0, 255, 0, 0),
)
device = uinput.Device(events)

class Test():
    def emit(self, key, value):
        print(key, value)

device = Test()

class ADC():
    def __init__(self, channel, addr=0x48):
        self.bus = smbus.SMBus(1)
        self.address = addr
        self.channel = channel + 0x40

    def value(self): #channel
        self.bus.read_byte_data(self.address, self.channel)
        return self.bus.read_byte_data(self.address, self.channel)

def create_cb(pin, key):
    def cb(ch):
        if GPIO.input(pin) == 0:
            device.emit(key, 1)
        else:
            device.emit(key, 0)
    return cb

GPIO.setmode(GPIO.BCM)
GPIO.setup(DPAD_UP, GPIO.IN)
GPIO.setup(DPAD_DOWN, GPIO.IN)
GPIO.setup(DPAD_LEFT, GPIO.IN)
GPIO.setup(DPAD_RIGHT, GPIO.IN)
GPIO.setup(A, GPIO.IN)
GPIO.setup(B, GPIO.IN)
GPIO.setup(X, GPIO.IN)
GPIO.setup(Y, GPIO.IN)
GPIO.setup(TL, GPIO.IN)
GPIO.setup(TR, GPIO.IN)
GPIO.setup(TL2, GPIO.IN)
GPIO.setup(TR2, GPIO.IN)
GPIO.setup(START, GPIO.IN)
GPIO.setup(SELECT, GPIO.IN)

DPAD_UP_cb = create_cb(DPAD_UP, uinput.BTN_DPAD_UP)
DPAD_DOWN_cb = create_cb(DPAD_DOWN, uinput.BTN_DPAD_DOWN)
DPAD_LEFT_cb = create_cb(DPAD_LEFT, uinput.BTN_DPAD_LEFT)
DPAD_RIGHT_cb = create_cb(DPAD_RIGHT, uinput.BTN_DPAD_RIGHT)
A_cb = create_cb(A, uinput.BTN_A)
B_cb = create_cb(B, uinput.BTN_B)
X_cb = create_cb(X, uinput.BTN_X)
Y_cb = create_cb(Y, uinput.BTN_Y)
TL_cb = create_cb(TL, uinput.BTN_TL)
TR_cb = create_cb(TR, uinput.BTN_TR)
TL2_cb = create_cb(TL2, uinput.BTN_TL2)
TR2_cb = create_cb(TR2, uinput.BTN_TR2)
START_cb = create_cb(START, uinput.BTN_START)
SELECT_cb = create_cb(SELECT, uinput.BTN_SELECT)

GPIO.add_event_detect(DPAD_UP, GPIO.BOTH, callback=DPAD_UP_cb)
GPIO.add_event_detect(DPAD_DOWN, GPIO.BOTH, callback=DPAD_DOWN_cb)
GPIO.add_event_detect(DPAD_LEFT, GPIO.BOTH, callback=DPAD_LEFT_cb)
GPIO.add_event_detect(DPAD_RIGHT, GPIO.BOTH, callback=DPAD_RIGHT_cb)
GPIO.add_event_detect(A, GPIO.BOTH, callback=A_cb)
GPIO.add_event_detect(B, GPIO.BOTH, callback=B_cb)
GPIO.add_event_detect(X, GPIO.BOTH, callback=X_cb)
GPIO.add_event_detect(Y, GPIO.BOTH, callback=Y_cb)
GPIO.add_event_detect(TL, GPIO.BOTH, callback=TL_cb)
GPIO.add_event_detect(TR, GPIO.BOTH, callback=TR_cb)
GPIO.add_event_detect(TL2, GPIO.BOTH, callback=TL2_cb)
GPIO.add_event_detect(TR2, GPIO.BOTH, callback=TR2_cb)
GPIO.add_event_detect(START, GPIO.BOTH, callback=START_cb)
GPIO.add_event_detect(SELECT, GPIO.BOTH, callback=SELECT_cb)

joystick_left_x = ADC(joystick_left_x_channel)
joystick_left_y = ADC(joystick_left_y_channel)
joystick_right_x = ADC(joystick_right_x_channel)
joystick_right_y = ADC(joystick_right_y_channel)

while True:
    joystick_left_x_value = joystick_left_x.value()
    joystick_left_y_value = joystick_left_y.value()
    joystick_right_x_value = joystick_right_x.value()
    joystick_right_y_value = joystick_right_y.value()

    if joystick_left_x_last != joystick_left_x_value:
        joystick_left_x_last = joystick_left_x_value
        device.emit(uinput.ABS_X, joystick_left_x_value)
    if joystick_left_y_last != joystick_left_y_value:
        joystick_left_y_last = joystick_left_y_value
        device.emit(uinput.ABS_Y, joystick_left_y_value)
    if joystick_right_x_last != joystick_right_x_value:
        joystick_right_x_last = joystick_right_x_value
        device.emit(uinput.ABS_RX, joystick_right_x_value)
    if joystick_right_y_last != joystick_right_y_value:
        joystick_right_y_last = joystick_right_y_value
        device.emit(uinput.ABS_RY, joystick_right_y_value)

