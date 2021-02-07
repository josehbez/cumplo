from bm import api
from bm.api import API
from django.urls import path , include

from . import views
from . import api

urlpatterns = [
    
    path('',views.HomePageView.as_view(), name='Home'),
    path('api/historical', api.API.Historical, name='Home'),
    path('api/dollar',  views.HomePageView.as_view(), name='Home'),
    path('api/udis',  views.HomePageView.as_view(), name='Home'),
    path('api/tiie',  views.HomePageView.as_view(), name='Home'),
    
]