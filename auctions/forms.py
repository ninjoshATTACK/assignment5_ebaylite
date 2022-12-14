from xml.etree.ElementTree import Comment
from django import forms
from .models import Bid, Listing, Comment

# Create your forms here.
class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('title', 'desc', 'startbid', 'photo_url', 'listing_category')

class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ('price',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)