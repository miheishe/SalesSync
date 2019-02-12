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


        all_info = requests.get('https://api.vk.com/method/execute', params={
            'v': '5.92',
            'access_token': settings.VK_ACCESS_TOKEN,
            'code': '''
                    var photos = API.photos.get({
                         "owner_id": "-140432051",
                         "album_id": "260801467",
                         "rev": 1,
                         "offset": 0,
                         "count": 1000,
                         "v": 5.92});
                        
                        var ids = photos.items@.id;
                        
                        var lastitem = photos.items.length - 1;
                
                        var id = photos.items[lastitem].sizes;
                        var id2 = id[id.length - 1].url;
                        
                        var links = photos.items@.sizes;
                        
                        var ret;
                        var ret2;
                        var i = 0;
                        while (i < links.length)
                        {
                        a = ids[i];
                        ret = {a : links[i][links.length -1].url};
                        //ret2 = ret2 + ret;
                        i = i + 1;
                        }
                        
                        return ret;
                        '''
        }).json()


        print(all_info)
