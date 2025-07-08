import time
import board
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Inicializa o teclado e o layout
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# --- Função para digitar em ABNT2 ---
def digitar_string_abnt2(string):
    print(f"Digitando: {string}")
    for char in string:
        if char == ':':
            # ==================== CORREÇÃO AQUI ====================
            # Para fazer ":", pressionamos SHIFT + a tecla que no layout ABNT2
            # tem ; e : (que no layout US é a tecla /).
            kbd.press(Keycode.SHIFT, Keycode.FORWARD_SLASH)
            kbd.release_all()
            # =======================================================
        elif char == '/':
            # Esta parte já está funcionando!
            # Em ABNT2, "/" é AltGr (Right Alt) + Q
            kbd.press(Keycode.RIGHT_ALT, Keycode.Q)
            kbd.release_all()
        else:
            # Para todos os outros caracteres, usamos o layout normal
            layout.write(char)
        
        time.sleep(0.01)

# -------------------------------------------

# Aguarda o PC reconhecer o dispositivo
time.sleep(1)

# Abre o terminal
print("Abrindo o terminal...")
kbd.press(Keycode.CONTROL, Keycode.ALT, Keycode.T)
kbd.release_all()

# Pausa para GARANTIR que o terminal seja a janela ativa.
print("Aguardando o foco do terminal...")
time.sleep(0.1)

# Define a string que queremos digitar
comando = "curl http://8.8.8.8"

# Usa a nossa nova função para digitar o comando corretamente
digitar_string_abnt2(comando)

# Pressiona Enter para executar o comando
kbd.press(Keycode.ENTER)
kbd.release_all()

digitar_string_abnt2("exit")
kbd.release_all()
kbd.press(Keycode.ENTER)
kbd.release_all()

print("Código concluído.")