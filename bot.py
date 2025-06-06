import sys
import time
import os
import pyautogui

ALCH_TIMEOUT = 3
TELE_ALCH_TIMEOUT = 3.2
POSITION_STALL = (589, 605)
POSITION_ITEMS = (1478, 801)
ALCH_POSITION = (1615, 882)
STOP_POSITION = (1159, 470)
STOP_PIXEL_COLOR = "03e9a9"


def alch():
    print("time:", time.ctime())
    pyautogui.moveTo(*ALCH_POSITION)
    pyautogui.click(button="left")


def alch_tele_camelot():
    print("time:", time.ctime())
    pyautogui.moveTo(1615, 882)
    pyautogui.click(button="left")
    time.sleep(0.8)
    pyautogui.moveTo(1590, 859)
    pyautogui.click(button="left")


def steal():
    def steal_stall():
        pyautogui.moveTo(*POSITION_STALL)
        print("moved mouse")
        pyautogui.click(button="left")
        print("left clicked")

    def steal_items():
        pyautogui.keyDown("shift")
        print("toggled shift down")
        pyautogui.moveTo(*POSITION_ITEMS)
        print("moved mouse")
        pyautogui.click(button="left")
        print("left clicked")
        pyautogui.keyUp("shift")
        print("toggled shift up")

    loop(steal_stall, 3)
    loop(steal_items, 4.5)


def scan():
    def take_screenshot():
        screenshot = pyautogui.screenshot()
        if not os.path.exists("input-images"):
            os.makedirs("input-images")
        path = os.path.join("input-images", f"screenshot_{int(time.time() * 1000)}.png")
        screenshot.save(path)

    def scan_interval():
        take_screenshot()
        check_for_stop_condition()
        x, y = pyautogui.position()
        print((x, y))
        pixel_color = pyautogui.screenshot().getpixel((x, y))
        print("%02x%02x%02x" % pixel_color)

    while True:
        scan_interval()
        time.sleep(0.2)


def loop(fn, sec):
    import random

    while True:
        fn()
        check_for_stop_condition()
        rand = sec + (random.randint(1, 6) * random.random())
        time.sleep(rand)


def check_for_stop_condition():
    print(STOP_PIXEL_COLOR)
    print(STOP_POSITION)
    screenshot = pyautogui.screenshot()
    pixel_color = screenshot.getpixel(STOP_POSITION)
    color_hex = "%02x%02x%02x" % pixel_color
    print("MUSIC BUTTON COLOR:", color_hex)
    if color_hex == STOP_PIXEL_COLOR:
        sys.exit()


def main():
    args = sys.argv[1:]
    if not args:
        print("invalid args")
        return
    if args[0] == "positions":
        scan()
    elif args[0] == "alch":
        loop(alch, ALCH_TIMEOUT)
    elif args[0] == "tele-alch":
        loop(alch_tele_camelot, TELE_ALCH_TIMEOUT)
    elif args[0] == "steal":
        steal()
    else:
        print("invalid args")


if __name__ == "__main__":
    main()
