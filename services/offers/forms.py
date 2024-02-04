from django import forms
from . import models
from offers.models import Comment


class OfferForm(forms.ModelForm):
    """Form to be displayed in create_offer and create request pages"""
    modifie_offer = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Offer
        fields = ['title', 'description', 'category', 'available']


class DeleteOfferForm(forms.Form):
    """Form displayed in view_offer page allowing the logged in user to delet his own offer"""
    delete_offer = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class CommentForm(forms.ModelForm):
    """Form displayed in modifie_comment page allowing the connected user to change or delete his own message"""
    modifie_comment = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Comment
        fields = ("comment_body",)
        widgets = {
            "comment_body": forms.Textarea(attrs={"class": "form-control"}),
        }
