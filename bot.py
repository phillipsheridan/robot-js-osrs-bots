import sys
import time
import os
import pyautogui
import requests
from dotenv import load_dotenv
import random

load_dotenv()  # Load variables from .env file
username = os.getenv("user")
password = os.getenv("password")

spellbook_clicked = False

ALCH_TIMEOUT = 2
TELE_ALCH_TIMEOUT = 3.2
POSITION_STALL = (589, 605)
POSITION_ITEMS = (1478, 801)
ALCH_POSITION = (1615, 882)
STOP_POSITION = (1159, 470)
STOP_PIXEL_COLOR = "03e9a9"


def human_like_move(x, y):

    move_duration = random.uniform(0.18, 0.45)
    jitter_x = random.randint(-8, 8)
    jitter_y = random.randint(-8, 8)
    pyautogui.moveTo(
        x + jitter_x,
        y + jitter_y,
        duration=move_duration,
        tween=pyautogui.easeInOutQuad,
    )
    time.sleep(0.2)


def move_near_cursor():
    time.sleep(0.2)
    x, y = pyautogui.position()
    x = x + random.randint(-8, 8)
    y = y + random.randint(-8, 8)
    human_like_move(x, y)


def alch():
    global spellbook_clicked
    print("time:", time.ctime())
    time.sleep(0.2)
    if not spellbook_clicked:
        click_template("spellbook.png")
    spellbook_clicked = True
    move_near_cursor()
    time.sleep(0.3)
    click_template("high-level-alch-spell.png")
    time.sleep(0.3)
    click_template("magic-longbows.png", 0.60)
    pyautogui.click(button="left")
    move_near_cursor()


def alch_tele_camelot():
    print("time:", time.ctime())
    human_like_move(1615, 882)
    pyautogui.click(button="left")
    time.sleep(0.8)
    human_like_move(1590, 859)
    pyautogui.click(button="left")


def steal():
    def steal_stall():
        human_like_move(*POSITION_STALL)
        print("moved mouse")
        pyautogui.click(button="left")
        print("left clicked")

    def steal_items():
        pyautogui.keyDown("shift")
        print("toggled shift down")
        human_like_move(*POSITION_ITEMS)
        print("moved mouse")
        pyautogui.click(button="left")
        print("left clicked")
        pyautogui.keyUp("shift")
        print("toggled shift up")

    loop(steal_stall, 3)
    loop(steal_items, 4.5)


def scan():
    while True:
        click_template()
        time.sleep(0.2)


def login():
    click_template("existing-user.png")
    time.sleep(0.2)
    pyautogui.typewrite(username, interval=0.1)
    time.sleep(0.2)
    click_template("password-input.png", 0.50)
    pyautogui.typewrite(password, interval=0.1)
    click_template("login.png", 0.50)
    human_like_move(30, 30)
    time.sleep(10)
    screenshot = take_screenshot()
    clickHereToPlayButtonPath = os.path.join("templates", "click-here-to-play.png")
    if template_found(screenshot, clickHereToPlayButtonPath):
        click_template("click-here-to-play.png")
        return True
    return False


def is_logged_out():
    screenshot = take_screenshot()
    existingUserPath = os.path.join("templates", "existing-user.png")
    if template_found(screenshot, existingUserPath):
        return True
    return False


def take_screenshot():
    screenshot = pyautogui.screenshot()
    if not os.path.exists("input-images"):
        os.makedirs("input-images")
    path = os.path.join("input-images", f"screenshot_{int(time.time() * 1000)}.png")
    screenshot.save(path)
    return path


from detect_image import (
    find_image_in_image,
    get_template_center_coordindates,
    template_found,
)


def click_template(template_name="login.png", threshold=0.99):
    screenshot_path = take_screenshot()
    x, y = pyautogui.position()
    print((x, y))
    screenshot_img = pyautogui.screenshot()
    width, height = screenshot_img.size
    if 0 <= x < width and 0 <= y < height:
        pixel_color = screenshot_img.getpixel((x, y))
        print("%02x%02x%02x" % pixel_color)
    else:
        print("Mouse position out of screenshot bounds")

    template_path = os.path.join("templates", template_name)
    if os.path.exists(template_path):
        # Strict template match
        if template_found(screenshot_path, template_path, threshold):
            try:
                coords, template_width, template_height = find_image_in_image(
                    screenshot_path, template_path
                )
                # Optionally, draw result and get center
                center_x, center_y = get_template_center_coordindates(
                    screenshot_path, coords, template_width, template_height, None
                )
                print(f"Template matched. Clicking center at ({center_x}, {center_y})")
                human_like_move(center_x, center_y)
                time.sleep(0.1)  # Small delay before clicking
                print("Clicking on the template:" + template_name)
                pyautogui.click(button="left")
            except Exception as e:
                print("Error in template matching logic:", e)
        else:
            print("Strict template match not found.")


def loop(fn, sec):
    import random

    logged_in = not is_logged_out()

    while True:
        if not logged_in:
            logged_in = login()
        else:
            # check for login screen
            logged_in = not is_logged_out()
        fn()
        rand = sec + (random.randint(1, 6) * random.random())
        time.sleep(rand)


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
