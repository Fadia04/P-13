from django.db import models
from django.conf import settings


class Category(models.Model):
    """Model for the categories with a single field required"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Offer(models.Model):
    """Model for the offers different fields required or not"""
    title = models.CharField(max_length=300)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.URLField(null=True, blank=True)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category", default=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="offers"
    )
    type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.title} {self.category.name} {self.description} {self.type}"


class Comment(models.Model):
    """Model for the comments with required fields"""
    offer = models.ForeignKey(
        Offer, related_name="comments", on_delete=models.CASCADE
    )
    commenter_name = models.CharField(max_length=200)
    comment_body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return f"{self.offer.title} {self.user.username} {self.commenter_name}"
