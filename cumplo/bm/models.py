from django.db import models


class Serie(models.Model):

    date = models.DateField("Date Publish")
    value = models.FloatField("Value")
    serie = models.CharField("Serie ID", max_length=10)