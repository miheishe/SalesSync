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

class CommentsForTeamplate(object):

    def __init__(self, datetime, user_id, text, like):
        self.datetime = datetime
        self.user_id = user_id
        self.text = text
        self.like = like

@transaction.atomic
def test(request):
    return HttpResponse([item.name for item in list(WaContact.objects.all())])


def albums_list(request):

    photos = requests.get('https://api.vk.com/method/photos.get', params={
        'access_token': settings.VK_ACCESS_TOKEN,
        'owner_id': '-140432051',
        'album_id': '258600569',
        'rev': 1,
        'offset': 0,
        'count': 1000,
        'v': '5.92'
    }).json()['response']['items']

    comments = requests.get('https://api.vk.com/method/photos.getAllComments', params={
        'owner_id': '-140432051',
        'album_id': '258600569',
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


    updcomment =[]
    for comment in comments:
        comment['photolink'] = photoslist[comment['pid']]
        comment['time'] = datetime.utcfromtimestamp(comment['date']).strftime('%Y-%m-%d %H:%M:%S')
        updcomment.append(comment)

    return render(request, 'sync/index.html', context={'comments': updcomment})
    # return HttpResponse(comments_list[4].text)


# def album_detail(request, slug):
#     album = Post.objects.get(slug__iexact=slug)
#     return render(request, 'blog/post_detail.html', context={'post': album})
