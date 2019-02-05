from django.shortcuts import render
from datetime import datetime
from django.db import transaction
from django.http import HttpResponse
from SalesSync import settings
from sync.models import WaContact
from sync.models import ShopProduct, ShopProductImages, ShopProductParams
# from sync.models import CommentsForTeamplate
import requests
# from django.http import HttpResponse


@transaction.atomic
def test(request):
    return HttpResponse([item.name for item in list(WaContact.objects.all())])


def albums_list(request):

    photos = requests.get('https://api.vk.com/method/photos.get', params={
        'access_token': settings.VK_ACCESS_TOKEN,
        'owner_id': '-140432051',
        'album_id': '260346218',
        'rev': 1,
        'offset': 0,
        'count': 1000,
        'v': '5.92'
    }).json()['response']['items']

    comments = requests.get('https://api.vk.com/method/photos.getAllComments', params={
        'owner_id': '-140432051',
        'album_id': '260346218',
        'need_likes': 1,
        'offset': 0,
        'count': 10000,
        'v': '5.92',
        'access_token': settings.VK_ACCESS_TOKEN,
    }).json()['response']['items']

    print(photos)
    print(comments)


    photoslist = {}
    for photo in photos:
        photoslist[photo['id']] = photo['sizes'][2]['url']


    users_ids = set()
    for comment in comments:
        users_ids.add(str(comment['from_id']))

    users_ids_list = ','.join(users_ids)


    users = requests.get('https://api.vk.com/method/users.get', params={
        'user_ids': users_ids_list,
        'fields': 'first_name, last_name',
        'name_case': 'nom',
        'v': '5.92',
        'access_token': settings.VK_ACCESS_TOKEN
        }).json()['response']

    users_ids_names ={}
    for user in users:
        users_ids_names[user['id']] = user['first_name'] + ' ' + user['last_name']


    print(users)


    updcomment =[]
    for comment in comments:
        comment['photolink'] = photoslist[comment['pid']]
        comment['time'] = datetime.utcfromtimestamp(comment['date']).strftime('%Y-%m-%d %H:%M:%S')
        comment['username'] = users_ids_names[comment['from_id']]
        updcomment.append(comment)

    return render(request, 'sync/index.html', context={'comments': updcomment})
    # return HttpResponse(comments_list[4].text)


# def album_detail(request, slug):
#     album = Post.objects.get(slug__iexact=slug)
#     return render(request, 'blog/post_detail.html', context={'post': album})
