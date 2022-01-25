from django.db import models
from django.contrib.auth.models import AbstractUser 
from cities_light.models import Country
from cities_light.models import City

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)    
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    credit = models.IntegerField(blank=True, null=True, default=0)
    
    def __str__(self):
        return self.email