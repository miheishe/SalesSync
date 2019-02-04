# -*- coding: utf-8 -*-
import os
import requests

from django.conf import settings


def upload_file_to_group_album(album_id, caption, download_url, file, filename,
                               group_id):
    upload_url = get_upload_url(album_id, group_id)
    with open(filename, "wb") as f:
        f.write(file)
    # Подготавливаем файл для отправки и отправляем его
    stream = open(filename, "rb")
    print((f'size: {os.path.getsize(filename)}'
           f'caption {caption} filename {filename} upload  {download_url}'))
    files = {'file1': stream}
    response = requests.post(upload_url, files=files).json()
    # Подтверждаем сохранение файла и получаем его данные в виде json
    aid_ = response['aid']
    result_json = requests.get('https://api.vk.com/method/photos.save',
                               params={
                                   'access_token': settings.VK_ACCESS_TOKEN,
                                   'album_id': aid_,
                                   'group_id': response['gid'],
                                   'server': response['server'],
                                   'photos_list': response['photos_list'],
                                   'caption': caption,
                                   'hash': response['hash'],
                                   'v': '5.92'
                               }).json()
    print(result_json)


def get_upload_url(album_id, group_id):
    response = requests.get(
        'https://api.vk.com/method/photos.getUploadServer', params={
            'access_token': settings.VK_ACCESS_TOKEN,
            'album_id': album_id,
            'group_id': group_id,
            'v': '5.52'
        }).json()
    server = response['response']['upload_url']
    return server
