from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from .models import User, Listing, Category, Comment, Bid
from .forms import ListingForm, BidForm

############Index Section (displays active listings)####################
def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all()
    })

######################Create Listing Section####################
#class ListingForm(forms.Form):         -----Moved this to forms.py
    #title = forms.CharField(label = "title")
    #price = forms.CharField(label = "price")
    #desc = forms.CharField(label = "desc")
    #category = forms.CharField(label = "category")

def create(request):
    if request.method == "POST":
        listing_form = ListingForm(request.POST, request.FILES)
        message = ""

        if listing_form.is_valid():
            new_listing = listing_form.save(commit=False)
            new_listing.seller = request.user  # works now
            new_listing.save()
            messages.success(request, (f'\"{ listing_form.cleaned_data["title"] }\" was successfully added!'))
            return redirect("index")

        else:
            message = "Invalid form, try again."
            return render(request, "auctions/create.html",{
                "listing_form": listing_form,
                "message": message
            })

        # TODO: for when I flesh out bidding in models.py

    else:
        listing_form = ListingForm()
    listings = Listing.objects.all()

    return render(request, "auctions/create.html",{
        "categories": Category.objects.all(),
        "listing_form": listing_form,
        'listings': listings
    })

################Listings Section####################
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    return render(request, "auctions/listing.html", {
        'listing': listing
    })

#################Bidding Section####################
def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    message = ""

    if request.method == "POST":
        bid_form = BidForm(request.POST)

        if bid_form.is_valid():
            new_bid = bid_form.save(commit=False)
            if (new_bid.price > listing.startbid):
                new_bid.buyer = request.user
                new_bid.listing = listing
                new_bid.save()
                listing.startbid = new_bid.price
                listing.save()
                return redirect('listing', listing_id=listing_id)
            else:
                message = "Something went wrong with the bid (your bid must be higher than current price)"
                return render(request, "auctions/bid.html", {
                    "bid_form": bid_form,
                    "message": message,
                })

    else:
        bid_form = BidForm()

    return render(request, "auctions/bid.html", {
        'bid_form': bid_form,
        "listing": listing,
    })

############Login/Logout Section####################
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
