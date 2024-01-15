import requests
from PIL import Image
from io import BytesIO
from rembg import remove

def remove_background(image_url):
    response = requests.get(image_url)
    input_image = Image.open(BytesIO(response.content))

    output_image = remove(input_image)

    buffered = BytesIO()
    output_image.save(buffered, format="PNG")
    buffered.seek(0)

    return buffered