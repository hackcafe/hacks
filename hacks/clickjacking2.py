def clickjacking2():
    from pynput.mouse import Listener
    import random
    import pyautogui

    def on_move(x, y):
        pass

    def on_click(x, y, button, pressed):
        if pressed:
            pyautogui.click(random.randint(1, 1400), random.randint(1, 850))

    def on_scroll(x, y, dx, dy):
        pass

    with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()