import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
import pytesseract
from text_detection import OCRProcessor

pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize the WindowCapture class
wincap = WindowCapture('File Explorer')

loop_time = time()
while True:
    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    if screenshot is None or screenshot.size == 0:
        print("Failed to capture screenshot")
        continue

    ocr_processor = OCRProcessor(screenshot)
    
    text = ocr_processor.extract_text()
    print(f"Extracted Text: {text}")
    
    # Draw bounding boxes and get the updated image
    boxed_image = ocr_processor.draw_boxes()

    if boxed_image is None or boxed_image.size == 0:
        print("Failed to draw boxes on screenshot")
        continue

    # Display the image with bounding boxes
    cv.imshow('Computer Vision', boxed_image)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
