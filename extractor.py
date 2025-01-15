from PIL import Image
from parser import PrescriptionParser
import easyocr
import cv2
import numpy as np

def extract(file_path):
    # Open the image file
    image = Image.open(file_path)

    # Preprocess the image
    processed_image = preprocess_image(image)

    # Use EasyOCR to extract text from the image
    reader = easyocr.Reader(['en'])
    results = reader.readtext(processed_image, paragraph=True, x_ths=0)
    
    document_text = "\n".join([result[1] for result in results])
    
    # Use the PrescriptionParser to extract fields as needed
    extracted_data = PrescriptionParser(document_text).parse()
    return extracted_data

def preprocess_image(img):
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    # processed_image = cv2.adaptiveThreshold(
    #     resized,
    #     255,
    #     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #     cv2.THRESH_BINARY,
    #     65, # block size 
    #     13  # constant
    # )
    return resized

if __name__ == "__main__":
    # Example usage with a sample PNG file
    data = extract("backend/resources/omeprazole-new.png")
    for key, value in data.items():
        print(f"{key}: {value}")

