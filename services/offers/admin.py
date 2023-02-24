from django.contrib import admin
from offers.models import Offer
from offers.models import Category


# Register your models here.
admin.site.register(Offer)
admin.site.register(Category)