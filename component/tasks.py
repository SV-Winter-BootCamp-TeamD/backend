from celery import shared_task
from .AI_utils import generate_image

@shared_task
def ai_execute(prompt, image_count, image_type):
    images_urls = generate_image(prompt, image_count, image_type)
    return images_urls