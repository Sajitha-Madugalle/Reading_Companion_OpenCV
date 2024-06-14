import cv2 as cv
import numpy as np
import os
from time import time, sleep
from windowcapture import WindowCapture
import pytesseract
from text_detection import OCRProcessor
import google.generativeai as genai

window = str(input("Enter the window name: "))

# Configure the Gemini API
genai.configure(api_key='AIzaSyCiWyhbRpi2FdtQrvI7MmxBtlFECm0ii4Y')
model = genai.GenerativeModel('gemini-1.0-pro-latest')

# Change the working directory to the folder this script is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize the WindowCapture class
wincap = WindowCapture(window)

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
            response = model.generate_content("Find important topics in this text: " + text)
            print(response.text.split('\n'))
        except Exception as e:
            print(f"Error processing text with Gemini API: {e}")
    else:
        print("No text extracted from screenshot.")
    
    # Press 'q' with the output window focused to exit
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    # Wait for 30 seconds before capturing the next screenshot
    sleep(10)

print('Done.')