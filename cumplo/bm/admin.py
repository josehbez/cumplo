# -*- coding: utf-8 -*-
# Copyright (c) 2021 José Hbez 
from django.contrib import admin

from .models import Serie

class SerieAdmin(admin.ModelAdmin):
    list_display = ('serie', 'date', 'value')

admin.site.register(Serie,SerieAdmin)
