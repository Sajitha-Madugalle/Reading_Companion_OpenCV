import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
from windowcapture import WindowCapture
from text_detection import OCRProcessor
import google.generativeai as genai
import pygetwindow as gw

# Configure the Gemini API
genai.configure(api_key='AIzaSyCiWyhbRpi2FdtQrvI7MmxBtlFECm0ii4Y')
model = genai.GenerativeModel('gemini-1.0-pro-latest')

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Window Capture App")

        # Set up the UI
        self.create_widgets()
        self.selected_window = None
        self.wincap = None
        self.prev_response = ""

        # Fetch and display open windows
        self.refresh_window_list()

    def create_widgets(self):
        # Frame for window selection
        self.left_frame = tk.Frame(self, width=200, height=400)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        self.left_frame.grid_propagate(False)

        # Frame for output display
        self.right_frame = tk.Frame(self, width=400, height=400)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
        self.right_frame.grid_propagate(False)

        # Window selection
        self.window_label = tk.Label(self.left_frame, text="Select Window Number:")
        self.window_label.pack(pady=5)
        self.window_number = tk.Entry(self.left_frame)
        self.window_number.pack(pady=5)
        self.select_button = tk.Button(self.left_frame, text="Go", command=self.select_window)
        self.select_button.pack(pady=5)

        # Refresh windows button
        self.refresh_button = tk.Button(self.left_frame, text="Refresh Windows", command=self.refresh_window_list)
        self.refresh_button.pack(pady=5)

        # Listbox to display windows
        self.window_listbox = tk.Listbox(self.left_frame)
        self.window_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

        # Output display
        self.output = scrolledtext.ScrolledText(self.right_frame, wrap=tk.WORD, width=50, height=20)
        self.output.pack(pady=5, fill=tk.BOTH, expand=True)

    def refresh_window_list(self):
        self.windows = gw.getAllTitles()
        self.windows = [win for win in self.windows if win]
        self.window_listbox.delete(0, tk.END)
        for i, window in enumerate(self.windows):
            self.window_listbox.insert(tk.END, f"{i + 1}. {window}")

    def select_window(self):
        try:
            window_number = int(self.window_number.get())
            if window_number < 1 or window_number > len(self.windows):
                messagebox.showerror("Error", "Invalid window number.")
                return
            self.selected_window = self.windows[window_number - 1]
            self.wincap = WindowCapture(self.selected_window)
            self.capture_and_process()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def capture_and_process(self):
        if not self.wincap:
            messagebox.showerror("Error", "No window selected.")
            return

        screenshot = self.wincap.get_screenshot()
        if screenshot is None or screenshot.size == 0:
            self.output.insert(tk.END, "Failed to capture screenshot\n")
            return

        ocr_processor = OCRProcessor(screenshot)
        text = ocr_processor.extract_text()
        
        self.output.delete(1.0, tk.END)  # Clear previous output

        if text.strip():
            try:
            # Process the text with Gemini API
                response = model.generate_content("find phrases to search in google, to get better undestand from this text" + text)
                new_response =  model.generate_content("identify similar ideas and only print one of them from these"+ "\n" + response.text + "\n" + self.prev_response)
                self.prev_response = response.text
                
                self.output.insert(tk.END, f"{new_response.text}\n")
            except Exception as e:
                self.output.insert(tk.END, f"Error processing text with Gemini API: {e}\n")
        else:
            self.output.insert(tk.END, "No text extracted from screenshot.\n")

        # Schedule next capture
        self.after(1000, self.capture_and_process)

if __name__ == "__main__":
    # Change the working directory to the folder this script is in
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = Application()
    app.mainloop()