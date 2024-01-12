from django.conf import settings
from openai import OpenAI

def generate_image(prompt, image_count, image_type):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    images_urls = []

    if image_type == "Background":
        size = "1792x1024"
    elif image_type == "Sticker":
        size = "1024x1024"
    else:
        size = "1024x1024"

    for _ in range(image_count):
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            n=1
        )
        image_url = response.data[0].url
        images_urls.append(image_url)

    return images_urls
