import cv2
from PIL import Image
import pytesseract

class OCRProcessor:
    def __init__(self, image):
        # Set the Tesseract command path
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # Read the image using OpenCV
        self.img_rgb = image
        self.imgH, self.imgW, _ = self.img_rgb.shape

    def extract_text(self):
        # Perform OCR to get the string
        self.img2char = pytesseract.image_to_string(self.img_rgb)
        return self.img2char

    def draw_boxes(self):
        # Perform OCR to get bounding boxes
        img2box = pytesseract.image_to_boxes(self.img_rgb)

        # Create a copy of the image to draw boxes on
        boxed_image = self.img_rgb.copy()

        # Draw rectangles around the recognized characters
        for boxes in img2box.splitlines():
            boxes = boxes.split(" ")
            x, y, w, h = int(boxes[1]), int(boxes[2]), int(boxes[3]), int(boxes[4])
            cv2.rectangle(boxed_image, (x, self.imgH - y), (w, self.imgH - h), (0, 0, 255), 3)

        return boxed_image
