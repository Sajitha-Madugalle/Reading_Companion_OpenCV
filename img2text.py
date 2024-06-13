import cv2
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt

# Set the tesseract command path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Read the image using OpenCV
img_rgb = cv2.imread('test.png')

# Display the original image using OpenCV
cv2.imshow('Original Image', img_rgb)
cv2.waitKey(0)  # Wait for a key press to close the image window

# Perform OCR to get the string
img2char = pytesseract.image_to_string(img_rgb)

# Perform OCR to get bounding boxes
img2box = pytesseract.image_to_boxes(img_rgb)

# Get the image dimensions
imgH, imgW, _ = img_rgb.shape

# Draw rectangles around the recognized characters
for boxes in img2box.splitlines():
    boxes = boxes.split(" ")
    x, y, w, h = int(boxes[1]), int(boxes[2]), int(boxes[3]), int(boxes[4])
    cv2.rectangle(img_rgb, (x, imgH - y), (w, imgH - h), (0, 0, 255), 3)

# Display the image with bounding boxes using OpenCV
cv2.imshow('Boxed Image', img_rgb)
cv2.waitKey(0)  # Wait for a key press to close the image window

# Clean up and close any OpenCV windows
cv2.destroyAllWindows()
