# Robot Car with Raspberry Pi Pico W BLE
# Modified from Official Rasp Pi example here:
# https://github.com/micropython/micropython/tree/master/examples/bluetooth
# Copyright Bernd54Albrecht
# This code is in the public domain and may be freely copied and used
# No warranty is provided or implied

import bluetooth
import time
from ble_advertising import advertising_payload
from micropython import const
from machine import Pin, PWM
import sys
import PIOpassiveBeep
# Initialisierung GPIO-Ausgang für Trigger-Signal
trigger = Pin(18, Pin.OUT)
# Initialisierung GPIO-Eingang für Echo-Signal
echo = Pin(19, Pin.IN)

beeper = PIOpassiveBeep.PIOBeep(0,16)
# frequencies of the notes, standard pitch (Kammerton a) is notes[5]=440 Hz
notes = [261, 293, 330, 349, 392, 440, 494, 523, 587, 659, 698, 784, 880, 988, 1046]

notes_val = []
for note in notes:
    notes_val.append(beeper.calc_pitch(note))

#the length the shortest note and the pause
note_len = 0.1
pause_len = 0.1

# Variable for buzz time
buzzTime = time.ticks_ms()

# Programmable IO (PIO) for blink
@rp2.asm_pio(set_init=(rp2.PIO.OUT_LOW))

def blink_1hz():
    # Cycles: 1 + 7 + 32 * (30 + 1) = 1000
    set(pins, 1)
    set(x, 31)                  [6]
    label("delay_high")
    nop()                       [29]
    jmp(x_dec, "delay_high")

    # Cycles: 1 + 7 + 32 * (30 + 1) = 1000
    set(pins, 0)
    set(x, 31)                  [6]
    label("delay_low")
    nop()                       [29]
    jmp(x_dec, "delay_low")

# Create and start a StateMachine with blink_1hz, outputting on Pin(14)
sm1 = rp2.StateMachine(1, blink_1hz, freq=2000, set_base=Pin(14))

## define 3 fragments of the code, idle is 16160
cy = 16     # forward/backward, digit 1 and 2
cx = 16     # left/right, digit 3 and 4
cb = 0      # button, digit 5 

def tutatatu():
    global buzzTime
    buzzTime = time.ticks_ms()    
    beeper.play_value(note_len*4, pause_len, notes_val[8])
    beeper.play_value(note_len*2, pause_len, notes_val[5])
    beeper.play_value(note_len*2, pause_len, notes_val[5])
    beeper.play_value(note_len*4, pause_len, notes_val[8])


# Initialisation of motors
vBatt = 6                # insert battery voltage
m1e = PWM(Pin(7))
m11 = Pin(8,Pin.OUT)
m12 = Pin(9,Pin.OUT)
m2e = PWM(Pin(12))
m21 = Pin(11,Pin.OUT)
m22 = Pin(10,Pin.OUT)
m1e.freq(1000)
m2e.freq(1000)
factor = 655.35 * 6/vBatt   # max PWM/100 * 6 / vBatt

# self-defined function for 2 motors with PWM
def motor(cy, cx):
    y = cy - 15   # forward/backward
    x = cx - 15   # left/right
    if y>=0:
        leftWheel = y + 0.5 * x
        rightWheel = y - 0.5 * x
    if y<0:
        leftWheel = y - 0.5 * x
        rightWheel = y + 0.5 * x    
    if leftWheel > 15:
        leftWheel = 15
    if leftWheel < -15:
        leftWheel = -15
    if rightWheel > 15:
        rightWheel = 15
    if rightWheel < -15:
        rightWheel = -15
    if leftWheel < -2:
        m11.off()
        m12.on()
    elif leftWheel > 2:
        m11.on()
        m12.off()
    else:
        m11.off()
        m12.off()
#        m1e.duty_u16(0)
    if rightWheel < -2:
        m21.off()
        m22.on()
    elif rightWheel > 2:
        m21.on()
        m22.off()
    else:
        m21.off()
        m22.off()
#        m2e.duty_u16(0)
    leftPWM = int(factor * (25 + 5*abs(leftWheel)))
    print("leftWheel = ",leftWheel," leftPWM = ", leftPWM)    
    rightPWM = int(factor * (25 + 5*abs(rightWheel)))
    print("rightWheel = ",rightWheel," rightPWM = ", rightPWM)    
    m1e.duty_u16(leftPWM)
    m2e.duty_u16(rightPWM)


## taken from ble_simple_peripheral.py
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_READ | _FLAG_NOTIFY,)
_UART_RX = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,)
_UART_SERVICE = (_UART_UUID,(_UART_TX, _UART_RX),)


class BLESimplePeripheral:
    def __init__(self, ble, name="PicoW"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._connections = set()
        self._write_callback = None
        self._payload = advertising_payload(name=name, services=[_UART_UUID])
        self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("New connection", conn_handle)
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_rx and self._write_callback:
                self._write_callback(value)

    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_tx, data)

    def is_connected(self):
        return len(self._connections) > 0

    def _advertise(self, interval_us=500000):
        print("Starting advertising")
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def on_write(self, callback):
        self._write_callback = callback

# This is the MAIN LOOP
def demo():    # This part modified to control Robot Car
    ble = bluetooth.BLE()
    p = BLESimplePeripheral(ble)

    def on_rx(code):  # code is what has been received
        code = str(code)[2:-5]	# necessary only for Smartphone APP
        code = int(code)
        cy = int(code/1000)             # digit 1 and 2
        cx = int((code-1000*cy)/10)     # digit 3 and 4
        cb = code - 1000*cy - 10*cx     # digit 5
        print("cy = ",cy," cx = ",cx," cb = ",cb)       # Print code fragments

        if cb & 1 == 1:
            print("blink")
            sm1.active(1)
        else:
            sm1.active(0)   

        if cb & 2 == 2: 
            print("tutatatu")
            ticksNow = time.ticks_ms()
            print("ticksNow = ", ticksNow)
            print("buzzTime = ", buzzTime)
            if time.ticks_diff(ticksNow,buzzTime) > 10000:
                tutatatu()
        else:
            pass

            
        if cb & 4 == 4:
            print("autonomous mode, not yet implemented")
            print("remote control instead")
            motor(cy,cx)       # call function motor with 2 parameters            
        else:
            print("remote control")
            motor(cy,cx)       # call function motor with 2 parameters
  
    p.on_write(on_rx)

if __name__ == "__main__":
    demo()
