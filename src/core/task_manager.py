# Path: src/core/task_manager.py

import os
import importlib.util

class TaskManager:
    """ Manages the tasks and their execution. """

    def __init__(self, tasks_path='./src/tasks', prompt_file='./assets/prompts/system_prompt.txt'):
        self.tasks_path = tasks_path
        self.task_handlers = self.load_task_handlers(tasks_path)
        self.prompt_file = prompt_file
    
    def load_system_prompt(self):
        """Load the basic system prompt from an external text file."""
        try:
            with open(self.prompt_file, 'r') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"The system prompt file '{self.prompt_file}' does not exist.")

    def build_system_prompt(self):
        """Build a dynamic system prompt with descriptions, triggers, and examples for each task."""
        #prompt = "You are a helpful assistant. Respond in JSON format based on the type of request.\n\n"
        prompt = self.load_system_prompt() + "\n\n"
        prompt += "The available tasks are as follows:\n"
        for task_name, task_info in self.task_handlers.items():
            prompt += f"Task: {task_name}\n"
            prompt += f"Description: {task_info['description']}\n"
            prompt += f"Trigger: {task_info['trigger']}\n"
            prompt += f"Example: {task_info['example']}\n\n"
        return prompt


    def load_task_handlers(self, tasks_path):
        """ Load all task handlers from specified directory. """
        handlers = {}
        for filename in os.listdir(tasks_path):
            if '__init__.py' in filename:
                continue

            if filename.endswith('.py'):
                task_name = filename[:-3]  # remove the '.py' extension
                module_path = os.path.join(tasks_path, filename)
                spec = importlib.util.spec_from_file_location(task_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                handlers[task_name] = {
                    'description': getattr(module, 'description', 'No description provided.'),
                    'trigger': getattr(module, 'trigger', 'No trigger provided.'),
                    'example': getattr(module, 'example', 'No example provided.'),
                    'execute': getattr(module, 'execute')
                }
        return handlers

    def execute_task(self, task_name, content):
        """ Execute a task based on task name. """
        if task_name in self.task_handlers:
            return self.task_handlers[task_name]['execute'](content)
        else:
            return f"Task {task_name} not found."