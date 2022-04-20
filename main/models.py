from django.db import models


class Item(models.Model):
    title = models.CharField("Наименование", max_length=150)
    price = models.DecimalField("Стоимость")
