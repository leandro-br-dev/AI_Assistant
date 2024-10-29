# Path: main.py

from tkinter import Tk
from src.gui.main_window import MainWindow

def main():
    """Main function to start the AI Assistant."""
    root = Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()