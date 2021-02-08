# -*- coding: utf-8 -*-
# Copyright (c) 2021 José Hbez. All rights reserved

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from . import api

class HomePageView(TemplateView):
    template_name = "home.html"
