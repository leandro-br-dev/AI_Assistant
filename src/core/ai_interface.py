# Path: src/core/ai_interface.py

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from src.core.task_manager import TaskManager

load_dotenv()

class AIInterface:
    """Handles interactions with the AI APIs."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.task_manager = TaskManager()

    def get_response(self, user_message):
        """Gets response from the AI based on user message."""
        try:
            system_prompt = self.task_manager.build_system_prompt()            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            json_response = json.loads(response.choices[0].message.content)
            response_type = json_response.get('type')
            response_content = json_response.get('content')
            return self.task_manager.execute_task(response_type, response_content)
        except Exception as e:
            return f"Sorry, I couldn't get a response. Please try again later. Error: {e}"