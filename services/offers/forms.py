from django import forms
from . import models

class OfferForm(forms.ModelForm):
    modifie_offer = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = models.Offer
        fields = ['title', 'description', 'category', 'available']
        
class DeleteOfferForm(forms.Form):
    delete_offer = forms.BooleanField(widget=forms.HiddenInput, initial=True)