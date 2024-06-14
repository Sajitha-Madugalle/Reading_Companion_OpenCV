import cv2 as cv
import numpy as np
import os
from time import time, sleep
from windowcapture import WindowCapture
import pytesseract
from text_detection import OCRProcessor
import google.generativeai as genai
import pygetwindow as gw

# Configure the Gemini API
genai.configure(api_key='AIzaSyCiWyhbRpi2FdtQrvI7MmxBtlFECm0ii4Y')
model = genai.GenerativeModel('gemini-1.0-pro-latest')

# Change the working directory to the folder this script is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Get a list of all open windows
windows = gw.getAllTitles()
windows = [win for win in windows if win]  # Remove empty window titles

# Display the list of windows to the user
print("Open windows:")
for i, window in enumerate(windows):
    print(f"{i + 1}. {window}")

# Prompt the user to select a window by number
window_number = int(input("Enter the number of the window you want to capture: "))
if window_number < 1 or window_number > len(windows):
    print("Invalid window number.")
    exit()

# Get the selected window title
selected_window = windows[window_number - 1]

# Initialize the WindowCapture class with the selected window
wincap = WindowCapture(selected_window)

while True:
    # Get an updated image of the window
    screenshot = wincap.get_screenshot()

    if screenshot is None or screenshot.size == 0:
        print("Failed to capture screenshot")
        continue

    ocr_processor = OCRProcessor(screenshot)
    
    text = ocr_processor.extract_text()
    
    if text.strip():
        try:
            # Process the text with Gemini API
            response = model.generate_content("find phrases to search in google, to get better undestand from this text" + text)
            print(response.text)
        except Exception as e:
            print(f"Error processing text with Gemini API: {e}")
    else:
        print("No text extracted from screenshot.")
    
    # Press 'q' with the output window focused to exit
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    # Wait for 30 seconds before capturing the next screenshot
    sleep(1)

print('Done.')
