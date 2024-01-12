import requests
from PIL import Image
import cv2
import numpy as np
from io import BytesIO
from rembg import remove

def post_process_image(image):
    kernel = np.ones((5,5), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.GaussianBlur(image, (5, 5), 0)
    return image

def remove_background(image_url):
    response = requests.get(image_url)
    input_image = Image.open(BytesIO(response.content))

    output_image = remove(input_image)

    opencv_image = cv2.cvtColor(np.array(output_image), cv2.COLOR_RGB2BGR)
    processed_image = post_process_image(opencv_image)

    final_image = Image.fromarray(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))

    buffered = BytesIO()
    final_image.save(buffered, format="PNG")
    buffered.seek(0)

    return buffered