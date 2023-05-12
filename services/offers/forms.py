from django import forms
from . import models
from offers.models import Comment

class OfferForm(forms.ModelForm):
    modifie_offer = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = models.Offer
        fields = ['title', 'description', 'category', 'available']
        
class DeleteOfferForm(forms.Form):
    delete_offer = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment_body",)
        widgets = {
            "comment_body": forms.Textarea(attrs={"class": "form-control"}),
        }
