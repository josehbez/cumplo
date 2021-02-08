# -*- coding: utf-8 -*-
# Copyright (c) 2021 José Hbez. All rights reserved

from bm import api
from bm.api import API
from django.urls import path , include

from . import views
from . import api

urlpatterns = [    
    path('',views.HomePageView.as_view(), name='Home'),
    path('api/historical', api.API.Historical),
    path('api/dollar',  api.API.Dollar,),
    path('api/udis',  api.API.Udis, ),
    path('api/tiie',  api.API.Tiie, ),    
]