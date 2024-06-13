import cv2
from PIL import Image
import pytesseract

class OCRProcessor:
    def __init__(self, image):
        # Set the Tesseract command path
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # Read the image using OpenCV
        self.img_rgb = image
        self.imgH, self.imgW, _ = self.img_rgb.shape

    def display_image(self, window_name='Image'):
        # Display the image using OpenCV
        cv2.imshow(window_name, self.img_rgb)
        cv2.waitKey(0)  # Wait for a key press to close the image window
        cv2.destroyAllWindows()

    def extract_text(self):
        # Perform OCR to get the string
        self.img2char = pytesseract.image_to_string(self.img_rgb)
        return self.img2char

    def draw_boxes(self):
        # Perform OCR to get bounding boxes
        img2box = pytesseract.image_to_boxes(self.img_rgb)

        # Draw rectangles around the recognized characters
        for boxes in img2box.splitlines():
            boxes = boxes.split(" ")
            x, y, w, h = int(boxes[1]), int(boxes[2]), int(boxes[3]), int(boxes[4])
            cv2.rectangle(self.img_rgb, (x, self.imgH - y), (w, self.imgH - h), (0, 0, 255), 3)

    def display_boxed_image(self, window_name='Boxed Image'):
        # Display the image with bounding boxes using OpenCV
        self.draw_boxes()
        cv2.imshow(window_name, self.img_rgb)
        cv2.waitKey(0)  # Wait for a key press to close the image window
        cv2.destroyAllWindows()