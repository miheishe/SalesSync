import requests
from django.conf import settings


def get_image_url(self, product):
    content = requests.get(
        f"http://yan-spb.tk/api.php/shop.product.images.getInfo",
        params={'id': product.image_id,
                'access_token': settings.WEBASSYST_ACCESS_TOKEN
                }).json()
    return content['original_filename'], content['url_big']