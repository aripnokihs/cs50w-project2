from django.contrib import admin
from .models import User, Listing, Category, Bid

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Bid)
# Register your models here.
