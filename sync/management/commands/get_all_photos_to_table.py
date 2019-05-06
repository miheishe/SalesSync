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
        albums = requests.get('https://api.vk.com/method/photos.getAlbums', params={
            'owner_id': '-140432051',
            'offset': 0,
            'need_system': 0,
            'need_covers': 0,
            'photo_sizes': 0,
            'v': '5.92',
            'access_token': settings.VK_ACCESS_TOKEN,
        }).json()['response']['items']
        print(albums)

        # with open('newfile.txt', 'w', encoding='win-1251') as g:
        #     d = int(input())
        #     print('1 / {} = {}'.format(d, 1 / d), file=g)
        with open('albums.csv', 'w', encoding='utf-8') as f:
            print('Photo ID; Album; URL; TEXT;',file=f)
            for album in albums:

                photos = []
                count = math.ceil(album['size'] / 1000)
                print(count)
                for offset_times in range(count):
                    photos += requests.get('https://api.vk.com/method/photos.get', params={
                        'owner_id': '-140432051',
                        'album_id': album['id'],
                        'rev': 0,
                        'photo_sizes': 1,
                        'offset': offset_times * 1000,
                        'count': 1000,
                        'v': '5.92',
                        'access_token': settings.VK_ACCESS_TOKEN,
                    }).json()['response']['items']
                    time.sleep(1)


                # print(photos)
                for photoItem in photos:
                    try:
                        print('{}; {}; {}; {};'.format(photoItem['id'],album['title'],photoItem['sizes'][-1]['url'],' '.join(photoItem['text'].split('\n'))),file=f)
                    except:
                        print(photoItem)
                time.sleep(1)

