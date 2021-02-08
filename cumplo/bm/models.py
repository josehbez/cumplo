# -*- coding: utf-8 -*-
# Copyright (c) 2021 José Hbez. All rights reserved

from django.db import models


class Serie(models.Model):

    date = models.DateField("Date Publish")
    value = models.FloatField("Value")
    serie = models.CharField("Serie ID", max_length=10)


    def __str__(self):
        return '%s , value: %s , date: %s '%(self.serie, self.value, self.date)