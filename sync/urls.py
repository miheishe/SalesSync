from django.urls import path
from django.conf.urls import url

from .views import *

urlpatterns = [
	path('', albums_list, name='albums_list'),
	url('add_like/', add_like, name='add_like'),
]