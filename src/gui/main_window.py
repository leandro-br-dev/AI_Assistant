# Path: src/gui/main_window.py

import tkinter as tk
from src.core.audio_handler import AudioHandler
from src.core.ai_interface import AIInterface

class MainWindow:
    """Represents the main application window."""

    def __init__(self, root):
        self.root = root
        self.audio_handler = AudioHandler()
        self.ai_interface = AIInterface()

        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface."""
        self.root.title("AI Assistant")
        self.root.geometry("600x400")

        # Chat display area
        self.chat_display = tk.Text(self.root, height=15, width=70, state='disabled', wrap='word', bg='lightgrey')
        self.chat_display.pack(pady=10)

        # User input area
        self.user_input = tk.Entry(self.root, width=50)
        self.user_input.pack(pady=5)
        self.user_input.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        # Record button
        self.record_button = tk.Button(self.root, text="Start Recording", command=self.toggle_recording)
        self.record_button.pack(pady=5)

    def display_message(self, message):
        """Displays a message in the chat display area."""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def send_message(self, event=None):
        """Handles sending a message."""
        user_message = self.user_input.get().strip()
        if user_message:
            self.display_message(f"You: {user_message}")
            self.user_input.delete(0, tk.END)
            response = self.ai_interface.get_response(user_message)
            self.display_message(f"AI Assistant: {response}")

    def toggle_recording(self):
        """Toggles audio recording."""
        if self.audio_handler.audio_stream:
            self.audio_handler.stop_recording()
            self.record_button.config(text="Start Recording")
        else:
            self.audio_handler.start_recording()
            self.record_button.config(text="Stop Recording")