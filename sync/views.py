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
    # comments_list = []
    comments = requests.get('https://api.vk.com/method/photos.getAllComments', params={
        'owner_id': '-140432051',
        'album_id': '258600569',
        'need_likes': 1,
        'offset': 0,
        'count': 10000,
        'v': '5.92',
        'access_token': settings.VK_ACCESS_TOKEN,
    }).json()['response']['items']

    # for comment in comments:
    #     a = CommentsForTeamplate
    #     a.user_id = comment['from_id']
    #     a.text = comment['text']
    #     a.datetime = comment['date']
    #     if comment['likes']['count'] != 0:
    #         a.like = True
    #     else:
    #         a.like = False

        # comments_list.append(a)

    # print(len(comments_list))
    # print(comments_list[4].text)

    return render(request, 'sync/index.html', context={'comments': comments})
    # return HttpResponse(comments_list[4].text)


# def album_detail(request, slug):
#     album = Post.objects.get(slug__iexact=slug)
#     return render(request, 'blog/post_detail.html', context={'post': album})
