from django.db import models

# Create your models here.

class Request(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.URLField(null=True)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} {self.description}"