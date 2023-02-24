from django.db import models
from django.conf import settings
#from services.requests.models import Request
# Create your models here.


    
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.name}"

class Offer(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.URLField(null=True)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category", default=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user"
    )
    def __str__(self):
        return f"{self.title} {self.category.name} {self.description}"   
    
class Comment(models.Model):
    offer = models.ForeignKey(
        Offer, related_name="comments", on_delete=models.CASCADE
    )
    commenter_name = models.CharField(max_length=200)
    comment_body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user"
    )
    def __str__(self):
        return f"{self.offer.title} {self.user.username} {self.commenter_name}"
