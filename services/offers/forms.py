from django import forms
from . import models
from offers.models import Comment

class OfferForm(forms.ModelForm):
    """Form to be displayed in create_offer and create_request pages"""
    modifie_offer = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = models.Offer
        fields = ['title', 'description', 'category', 'available']
        
class DeleteOfferForm(forms.Form):
    """Form displayed in modifie_offer page allowing the logged in user to delete his own offer"""
    delete_offer = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
class CommentForm(forms.ModelForm):
    """Form displayed in modifie_comment page allowing the connected user to change his own offer"""
    modifie_comment = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = Comment
        fields = ("comment_body",)
        widgets = {
            "comment_body": forms.Textarea(attrs={"class": "form-control"}),
        }
