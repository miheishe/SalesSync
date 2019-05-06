# -*- coding: utf-8 -*-
import requests
import time
from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction
import os
import math

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
        # print(albums)

        #создаем каталог
        try:
            os.mkdir('Albums')
        except:
            print('Folder Albums already exist. Processing...')

        os.chdir('Albums')

        for num_albums, album in enumerate(albums,1):
            try:
                os.mkdir(album['title'])
                print('Creating {}.'.format(album['title']))
            except:
                print('Folder {} already exist. Processing...'.format(album['title']))

            os.chdir(album['title'])

            # альбом возвращает size - количество фотографий в альбоме

            photos = []
            count = math.ceil(album['size']/1000)
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

            for num_photo, photoItem in enumerate(photos, 1):
                try:
                    with open(str(photoItem['id'])+'.jpg', 'wb') as fpic:
                        picture = requests.get(photoItem['sizes'][-1]['url'])
                        fpic.write(picture.content)
                    with open(str(photoItem['id'])+'.txt', 'w', encoding='utf-8') as ftxt:
                        ftxt.write(' '.join(photoItem['text'].split('\n')))

                    print('Album {} / {}. Saved {} / {}'.format(num_albums, len(albums),num_photo, len(photos)))
                except Exception as err:
                    print(err)

            os.chdir('..')



