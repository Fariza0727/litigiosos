from django.db import models
from paymentintegration.authentication.models import User
from decimal import Decimal

from payments import PurchasedItem
from payments.models import BasePayment
from cities_light.models import Country
from cities_light.models import City

# Create your models here.

class Content(models.Model):
    title = models.CharField(max_length=100, blank=True,default="")
    username = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now=True, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='id_user',
                                blank=True, null=True, related_name='user_relationship')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)    
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    voting = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    category = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, blank=True, null=True)
    marks = models.IntegerField(null=True, blank=True, default=0)

class Commit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, blank=True, null=True)
    commit = models.TextField(blank=True)
    date = models.DateTimeField(auto_now=True, blank=True, null=True)

class ContentView(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    view = models.BooleanField(default=False)


# class Payment(BasePayment):

#     def get_failure_url(self):
#         return 'http://example.com/failure/'

#     def get_success_url(self):
#         return 'http://example.com/success/'

#     def get_purchased_items(self):
#         # you'll probably want to retrieve these from an associated order
#         yield PurchasedItem(name='The Hound of the Baskervilles', sku='BSKV',
#                             quantity=9, price=Decimal(10), currency='USD')