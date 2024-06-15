import os
import tkinter as tk # for the GUI
from tkinter import messagebox # for the GUI
import google.generativeai as genai # for using the generative model
import pygetwindow as gw # for getting the window titles
import webbrowser # for opening the browser

from windowcapture import WindowCapture # for capturing the window, see windowcapture.py
from text_detection import OCRProcessor # for processing the text, see text_detection.py


genai.configure(api_key='Your API')
# Load the generative model, Paste The API Key here,
# You can Find it in Google AI Studio
# https://aistudio.google.com/

model = genai.GenerativeModel('gemini-1.0-pro-latest') # Load the generative model

class Application(tk.Tk):
    """ Class to create the GUI window."""
    def __init__(self):
        super().__init__()
        self.title("Reading Companion") # Set the title of the window
        self.iconbitmap('iconRC.ico') # Set the icon of the window
        
        #self.wm_attributes("-topmost", True)
        #set if the windwo is always on the top
        
        self.create_widgets()
        self.selected_window = None
        self.window_capture = None
        self.previous_response = ""

        self.refresh_window_list()

    def create_widgets(self):
        """ Create the widgets for the GUI."""
        
        self.left_frame = tk.Frame(self, width=400, height=400)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns") 
        self.left_frame.grid_propagate(True) #adgust the left frame size

        self.right_frame = tk.Frame(self, width=400, height=400)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
        self.right_frame.grid_propagate(True) #adgust the right frame size

        self.window_label = tk.Label(self.left_frame, text="Select Window Number:")
        self.window_label.pack(pady=5)
        self.window_number_entry = tk.Entry(self.left_frame)
        self.window_number_entry.pack(pady=5)
        self.select_button = tk.Button(self.left_frame, text="Go", command=self.select_window)
        self.select_button.pack(pady=5) 
        # selecting the window widget for the GUI

        self.refresh_button = tk.Button(self.left_frame, text="Refresh Windows", command=self.refresh_window_list)
        self.refresh_button.pack(pady=5)
        # refresh the window widget for the GUI

        self.window_listbox = tk.Listbox(self.left_frame, width=100, height=20)
        self.window_listbox.pack(pady=5, fill=tk.BOTH, expand=True)
        # listing windows widget for the GUI

        self.button_frame = tk.Frame(self.right_frame)
        self.button_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        # button for the GUI

    def refresh_window_list(self):
        """" Refresh the list of windows in the GUI."""
        self.windows = [win for win in gw.getAllTitles() if win]
        self.window_listbox.delete(0, tk.END)
        for i, window in enumerate(self.windows):
            self.window_listbox.insert(tk.END, f"{i + 1}. {window}")

    def select_window(self):
        """ Select the window based on the window number entered by the user."""
        try:
            window_number = int(self.window_number_entry.get())
            if window_number < 1 or window_number > len(self.windows):
                messagebox.showerror("Error", "Invalid window number.")
                return
            self.selected_window = self.windows[window_number - 1]
            self.window_capture = WindowCapture(self.selected_window)
            self.capture_and_process()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def capture_and_process(self):
        """ Capture the screenshot of the selected window and process the text."""
        if not self.window_capture:
            messagebox.showerror("Error", "No window selected.") # Error message if no window is selected
            return

        screenshot = self.window_capture.get_screenshot()
        if screenshot is None or screenshot.size == 0:
            messagebox.showerror("Error", "Failed to capture screenshot.")
            return # Error message if failed to capture screenshot

        ocr_processor = OCRProcessor(screenshot) # Process the text using OCR
        text = ocr_processor.extract_text() # Extract the text from the image
        
        for widget in self.button_frame.winfo_children():
            # Destroy the existing buttons in the search buttons
            # this will happen every 5 seconds, can change the time Go to line 129
            widget.destroy() 

        if text.strip():
            try:
                response = model.generate_content("Find phrases to search in Google to get a better understanding from this text: " + text)
                new_response = model.generate_content("Identify similar ideas and only print one of them from these:\n" + response.text + "\n" + self.previous_response)
                self.previous_response = response.text
                
                """This could be achieved by deep learning models, which can be used to generate text based on the input text.
                    Here Gemini API is used to generate text based on the input text. It get the extracted text then generates
                    a list of phrases to search in Google to get a better understanding.
                    
                    Again, it generates a list of similar ideas and only print one of them from these.
                    In this approch the results will converge to main idea, and it will be more accurate.
                    
                    Deep learning models definitely could be used to do the same thing"""
                
                
                self.create_search_buttons(new_response.text.split('\n')) # Create search buttons for the extracted text
                
            except Exception as e:
                tk.Label(self.button_frame, text=f"Error processing text with Gemini API: {e}").pack() # Error message if failed to process text
        else:
            tk.Label(self.button_frame, text="No text extracted from screenshot.").pack() # Error message if no text extracted

        #refresh the List
        self.after(5000, self.capture_and_process) # Capture and process the text every 5 seconds, can change the time.

    def create_search_buttons(self, texts):
        for text in texts:
            if text.strip():
                button = tk.Button(self.button_frame, text=text, command=lambda t=text: self.open_google_search(t))
                button.pack(pady=2, fill=tk.X) # Create search buttons for the extracted text

    def open_google_search(self, search_text):
        url = f"https://www.google.com/search?q={search_text}"
        webbrowser.open(url) # Open the Google search in the browser

if __name__ == "__main__":
    """ Run the application."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = Application()
    app.mainloop()
