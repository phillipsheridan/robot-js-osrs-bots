import sys
import time
import os
import pyautogui
import requests

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
        return path

    def click_template(template_name="login.png"):
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

        # Use Flask server for template matching
        template_path = os.path.join("templates", template_name)
        if os.path.exists(template_path):
            with open(screenshot_path, "rb") as src, open(template_path, "rb") as tmpl:
                files = {"source": src, "template": tmpl}
                try:
                    resp = requests.post(
                        "http://localhost:5000/detect", files=files, timeout=10
                    )
                    if resp.ok:
                        data = resp.json()
                        if "x" in data and "y" in data and "output_image" in data:
                            print("Template matched. Clicking thingy.")
                            # Try to get template width/height from output_image filename if possible
                            # But ideally, server.py should return width/height in the response
                            width = data.get("template_width")
                            height = data.get("template_height")
                            x = int(data["center_x"])
                            y = int(data["center_y"])
                            print(
                                f"Received x={x}, y={y}, width={width}, height={height}"
                            )
                            if width is not None and height is not None:
                                try:
                                    print(f"Clicking center at ({x}, {y})")
                                    pyautogui.moveTo(x, y)
                                except Exception as e:
                                    print("Error parsing width/height:", e)
                                    pyautogui.moveTo(x, y)
                            else:
                                pyautogui.moveTo(x, y)
                            pyautogui.click(button="left")
                except Exception as e:
                    print("Error calling server.py:", e)

    while True:
        click_template()
        time.sleep(0.2)


def loop(fn, sec):
    import random

    while True:
        fn()
        rand = sec + (random.randint(1, 6) * random.random())
        time.sleep(rand)


def main():
    args = sys.argv[1:]
    if not args:
        print("invalid args")
        return
    if args[0] == "positions":
        ##
        #  I am thinking of refactoring scan to "play"- it will take a json object as the "playbook" - which includes step conditions, and an array of "step" that the bot will loop through using the step conditions to guide it. Basically a state machine. And so an example playbook could be:
        ### {
        #     "name": "high alch",
        #     "steps": [ click existing user, click login inputs and login. click high alch, click items, click alch, click stop ],
        # state conditions: [ "is logged in", "has items to alch", "is at alch interface" ]

        # stop condition: "is login screen detected"
        ##

        # maybe playbooks can contain common actions too like callback for like login, open-bag, click rune(r), etc.
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
