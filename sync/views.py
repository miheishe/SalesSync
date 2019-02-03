from django.shortcuts import render
from datetime import datetime
from django.db import transaction
from django.http import HttpResponse
from SalesSync import settings
from sync.models import WaContact
from sync.models import ShopProduct, ShopProductImages, ShopProductParams
import requests

@transaction.atomic
def test(request):
    return HttpResponse([item.name for item in list(WaContact.objects.all())])


def albums_list(request):
    comments = requests.get('https://api.vk.com/method/photos.getAllComments', params={
        'owner_id': '-140432051',
        'album_id': '258600569',
        'need_likes': 1,
        'offset': 0,
        'count': 10000,
        'v': '5.92',
        'access_token': settings.VK_ACCESS_TOKEN,
    }).json()['response']['items']

    return render(request, 'sync/index.html', context={'comments': comments})


# def album_detail(request, slug):
#     album = Post.objects.get(slug__iexact=slug)
#     return render(request, 'blog/post_detail.html', context={'post': album})
