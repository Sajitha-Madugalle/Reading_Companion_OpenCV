import cv2 as cv
import os
from time import sleep
from windowcapture import WindowCapture
from text_detection import OCRProcessor
import google.generativeai as genai
import pygetwindow as gw

class SearchAI:
    def __init__(self):
        # Configure the Gemini API
        genai.configure(api_key='Your API')
        self.model = genai.GenerativeModel('gemini-1.0-pro-latest')
        
        # Change the working directory to the folder this script is in
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Get a list of all open windows
        self.windows = gw.getAllTitles()
        self.windows = [win for win in self.windows if win]  # Remove empty window titles
        
        self.selected_window = None
        self.wincap = None
        self.ocr_processor = None

    def select_window(self, index):
        self.selected_window = self.windows[index]
        self.wincap = WindowCapture(self.selected_window)

    def run_once(self):
        # Get an updated image of the window
        screenshot = self.wincap.get_screenshot()
        
        if screenshot is None or screenshot.size == 0:
            print("Failed to capture screenshot")
            return None
        
        self.ocr_processor = OCRProcessor(screenshot)
        text = self.ocr_processor.extract_text()
        
        if text.strip():
            try:
                # Process the text with Gemini API
                response = self.model.generate_content(
                    "find phrases to search in google, to get better understand from this text: " + text
                )
                return response.text
            except Exception as e:
                print(f"Error processing text with Gemini API: {e}")
                return f"Error processing text with Gemini API: {e}"
        else:
            return "No text extracted from screenshot."
