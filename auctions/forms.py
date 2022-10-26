from django import forms
from .models import Listing

# Create your forms here.
class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('title', 'desc', 'startbid', 'photo_url', 'listing_category')