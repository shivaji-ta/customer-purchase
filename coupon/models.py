from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=15, unique=True)
    description = models.TextField()
    discount = models.BigIntegerField()
