def clickjacking1():
    from pynput.mouse import Listener
    import random
    import pyautogui

    def on_move(x, y):
        pass

    def on_click(x, y, button, pressed):
        if pressed:
            pyautogui.click(x + random.randint(-10, 10), y + random.randint(-10, 10))

    def on_scroll(x, y, dx, dy):
        pass

    with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()