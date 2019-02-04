# -*- coding: utf-8 -*-
from datetime import datetime

import requests
from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction

from sync.api.vk import upload_file_to_group_album
from sync.models import ShopProductImages, ShopProduct


def post_photo(caption, download_url, filename):
    album_id = settings.VK_ALBUM_ID,
    group_id = settings.VK_GROUP_ID,

    file = requests.get(download_url, allow_redirects=True).content

    # Получаем адрес сервера для загрузки фотографии
    upload_file_to_group_album(album_id, caption, download_url, file, filename,
                               group_id)


@transaction.atomic
class Command(BaseCommand):
    transaction.atomic()

    def handle(self, *args, **kwargs):
        for product in ShopProduct.objects.all():
            if product.is_changed():
                images = list(
                    ShopProductImages.objects.filter(product_id=product.id))
                if images:
                    filename, url = self.get_image_url(product)
                    caption = f'{product.name}'
                    post_photo(caption, url, filename)
                    product.saved_date = datetime.now()


