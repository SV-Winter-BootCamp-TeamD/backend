import requests, os

def search_pixabay_images(keyword):
    url = "https://pixabay.com/api/"
    params = {
        "key": os.getenv('PIXABAY_API_KEY'),
        "q": keyword,
        "image_type": "photo",
        "orientation": "horizontal",
        "per_page": 10
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
