from django.contrib import admin
from .models import User, Listing, Category, Bid, Comment

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "starting_bid", "category", "creator", "is_open")

class BidAdmin(admin.ModelAdmin):
    list_display = ("listing", "bid_price", "bidder")

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
# Register your models here.
