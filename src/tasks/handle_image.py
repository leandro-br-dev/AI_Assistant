# Path: src/tasks/handle_image.py

description = "Handles requests related to images on the screen."
trigger = "If the user asks about the screen or image, use this task."
example = "{'type': 'handle_image', 'content': 'Question about the image'}"

import os
import base64
from io import BytesIO
from PIL import Image
import mss
from openai import OpenAI

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

def ler_tela(content):
    """Processes the screen content based on AI response."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    image = capture_screen(800, 600, monitor_index=2)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": content},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "data:image/png;base64," + base64_image,
                        }
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    return response.choices[0].message.content

def execute(content):
    """Execute the image handling task."""
    print(f"Handling image task: {content}")
    resposta = ler_tela(content)
    return resposta