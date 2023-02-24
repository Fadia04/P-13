from django.db import models
from django.conf import settings
from offers.models import Offer
# Create your models here.

class Favorite(models.Model):
    name = models.CharField(max_length=200)
    offer = models.ForeignKey(
        Offer, null=True, on_delete=models.SET_NULL, related_name="favorite_offer"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user"
    )
 
    def __str__(self):
        return f"{self.name} {self.user.username}"
