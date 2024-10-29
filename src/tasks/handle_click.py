# Path: src/tasks/handle_click.py

description = "Handles clicking a part of the screen."
trigger = "If the user asks to click, run this task."
example = "{'type': 'handle_click', 'content': 'Click on ...'}"

import pyautogui
import mss
from PIL import Image
import replicate
import re
from io import BytesIO
import base64

def capture_screen(width=800, height=600, monitor_index=2):
    """Captures a portion of the screen."""
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_index]
        region = {
            "top": monitor["top"],
            "left": monitor["left"],
            "width": width,
            "height": height
        }
        screenshot = sct.grab(region)
        return Image.frombytes("RGB", screenshot.size, screenshot.rgb)

def click_on(content):
    """Executes the click action based on AI output."""
    segundo_monitor_pixels = 1920
    image = capture_screen(800, 600, monitor_index=2)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

    output = replicate.run(
        "zsxkib/molmo-7b:76ebd700864218a4ca97ac1ccff068be7222272859f9ea2ae1dd4ac073fa8de8",
        input={
            "text": content,
            "image": "data:image/png;base64," + base64_image,
            "top_k": 100,
            "top_p": 1,
            "temperature": 1,
            "length_penalty": 1,
            "max_new_tokens": 1000
        }
    )

    pattern = r'x\d*="([\d.]+)" y\d*="([\d.]+)"'
    matches = re.findall(pattern, output)
    coordinates = [(float(x), float(y)) for x, y in matches]

    for x, y in coordinates:
        pyautogui.moveTo(x + segundo_monitor_pixels, y, duration=0.5)
        pyautogui.click()

    return f"Clicked on the specified coordinates: {coordinates}"

def execute(content):
    """Execute the click task."""
    print(f"Handling click task: {content}")
    return click_on(content)