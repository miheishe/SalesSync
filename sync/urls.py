from django.urls import path

from .views import *

urlpatterns = [
	path('', albums_list, name='albums_list'),

	# path('album/<str:slug>/', album_detail, name='album_detail_url')
]