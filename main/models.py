from django.db import models


class Item(models.Model):
    title = models.CharField("Наименование", max_length=150)
    price = models.DecimalField("Стоимость", max_digits=10, decimal_places=2)


class Cheque(models.Model):
    cheque = models.FileField("PDF чека", upload_to="cheques")
