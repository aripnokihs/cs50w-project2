from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import CharField
from django.forms import HiddenInput
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from unicodedata import category

from .models import User, Listing, Category, Bid, Comment

class Comment_form(forms.Form):
    content = forms.CharField(max_length=64, label="", widget=forms.Textarea(attrs={
        'class': 'form-control', 'style': 'width: 40%; height: 100px; margin-bottom: 10px;'}))

class Create_listing_form(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image", "category"]
        # widgets = {
        #     "description": forms.Textarea
        #
        # }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
            # self.fields['category'] = forms.ModelChoiceField(
            #     queryset=Category.objects.all(),
            #     label="CATEGORY",
            #     empty_label="Select a Category"
            # )
    title = forms.CharField(max_length=64, label="TITLE")
    description = forms.CharField(widget=forms.Textarea, max_length=1000, label="DESCRIPTION")
    starting_bid = forms.IntegerField(label="STARTING BID", widget=forms.NumberInput(attrs={'style': 'width: 200px;'}))
    image = forms.ImageField(label="IMAGE", widget=forms.FileInput(attrs={'style': 'width: 200px; height: 50px;'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="CATEGORY")
def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
def create_listing(request):
    if request.method == "POST":
        form = Create_listing_form(request.POST, request.FILES)
        if form.is_valid():
            # print("inside3")
            # print(form)
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            print(form.errors)
            messages.error(request, "There was an error creating your listing. Please try again.")
    return render(request, "auctions/create_listing.html", {
        "create_listing_form": Create_listing_form({'creator': request.user})
    })

def listing_page(request, listing_id):
    if request.method == "POST":
        print(request.POST.get("bid"))
        print(request.POST.get("close"))
        print(request.POST.get("comment"))
        if request.POST.get("bid") != None:
            bidder = request.user
            price = int(request.POST.get("bid_price"))
        # print(price, type(price))
            listing = Listing.objects.get(pk=listing_id)
        # print(listing.bid_price, type(listing.bid_price))
            if price < listing.bid_price:
                return render(request, "auctions/listing_page.html", {
                    "listing": listing,
                    "price_error": True,
                    "comment_form": Comment_form(),
                })
            new_bid = Bid(bidder=bidder, bid_price=price, listing=listing)
            new_bid.save()
        elif request.POST.get("close") != None:
            listing = Listing.objects.get(pk=listing_id)
            listing.is_open = False
            listing.save()
        elif request.POST.get("content") != None:
            content = request.POST.get("content")
            commenter = request.user
            listing = Listing.objects.get(pk=listing_id)
            new_comment = Comment(content=content, commenter=commenter,listing=listing)
            new_comment.save()
    listing = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "comment_form": Comment_form(),
    })

def watchlist(request):
    usr = User.objects.get(pk=request.user.id)
    if request.method == "POST":
        if request.POST.get("add") != None:
            listing_id = request.POST.get("add")
            listing = Listing.objects.get(pk=listing_id)
            # user_id = int(request.POST.get("user"))
            # usr = User.objects.get(pk=user_id)
            usr.watchlist.add(listing)
        elif request.POST.get("delete") != None:
            listing_id = request.POST.get("delete")
            listing = Listing.objects.get(pk=listing_id)
            # user_id = int(request.POST.get("user"))
            # usr = User.objects.get(pk=user_id)
            usr.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("watchlist"))
    return render(request, "auctions/watchlist.html", {
        "listings": usr.watchlist.all()
    })

def delete_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    listing_id = comment.listing.id
    comment.delete()
    return HttpResponseRedirect(reverse("listing_page", args=(listing_id, )))