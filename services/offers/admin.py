from django.contrib import admin
from offers.models import Offer
from offers.models import Category
from offers.models import Request
from offers.models import Comment


# Register your models here.
admin.site.register(Offer)
admin.site.register(Category)
admin.site.register(Request)
admin.site.register(Comment)