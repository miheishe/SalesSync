# -*- coding: utf-8 -*-
import requests
import time
from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction

from sync.models import ShopProduct, ShopProductImages


@transaction.atomic
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # VK_ACCESS_TOKEN = '3dafe3da022feb6f1b66b195f35840576cb830a47ba3005730937e242bd85d11fa99d9a2381cf56189d0d'
        # WEBASSYST_ACCESS_TOKEN = '89e6b8ede056a40eadd540228134b2a3'
        # VK_GROUP_ACCESS_TOKEN = 'a81677a7406d38026fb4748c6c41078e6578969d3aa622b60221aa9525fbc728d95169bb61f61a71baa7b'
        # VK_GROUP_ID = 175030782
        # VK_ALBUM_ID = 258677915

        # photo_id = '456239019'
        #
        # photos_ids = requests.get('https://api.vk.com/method/photos.get', params={
        #     'access_token': settings.VK_ACCESS_TOKEN,
        #     'owner_id': '-140432051',
        #     'album_id': '258600569',
        #     'rev': 1,
        #     'offset': 0,
        #     'count': 1000,
        #     'v': '5.92'
        # }).json()['response']['items']

        comments = requests.get('https://api.vk.com/method/photos.getAllComments', params={
            'owner_id': '-140432051',
            'album_id': '258600569',
            'need_likes': 1,
            'offset': 0,
            'count': 10000,
            'v': '5.92',
            'access_token': settings.VK_ACCESS_TOKEN,
        }).json()['response']['items']
        print(comments)

