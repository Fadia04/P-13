from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from . import forms
from django.shortcuts import get_object_or_404
from datetime import datetime
from offers.models import Offer, Category, Comment
from offers.forms import OfferForm, CommentForm
# Create your views here.

@login_required
def offer_creation(request):
    offer_form = forms.OfferForm()
    if request.method == 'POST':
        offer_form = forms.OfferForm(request.POST)
    
        if offer_form.is_valid():
            offer = offer_form.save(commit=False)
            offer.user = request.user
            offer.save()
            return redirect('home')
            
    context = {
        'offer_form': offer_form,
        
}
    return render(request, 'offers/create_offer.html', context=context)

@login_required
@permission_required('offers.modifie_offer', raise_exception=True)
def modifie_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    modifie_form = forms.OfferForm(instance=offer)
    delete_form = forms.DeleteOfferForm()
    if request.method == 'POST':
        if 'modifie_offer' in request.POST:
            modifie_form = forms.OfferForm(request.POST, instance=offer)
            if modifie_form.is_valid():
                modifie_form.save()
                return redirect('home')
            if 'delete_offer' in request.POST:
                delete_form = forms.DeleteOfferForm(request.POST)
                if delete_form.is_valid():
                    offer.delete()
                    return redirect('home')
    context = {
        'modifie_form': modifie_form,
        'delete_form': delete_form,
}
    return render(request, 'offers/modifie_offer.html', context=context)


def view_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    #offers = Offer.objects.all(id=offer_id)
    return render(request, 'offers/view_offer.html', {'offer': offer})


def view_offers(request):
    offers = Offer.objects.all()
    
    return render(request,'offers/view_offers.html', {'offers': offers})


def search(request):
    if request.method == "POST":
        query = request.POST["query"]
        offers = Offer.objects.filter(description__icontains=query).order_by("date_added")[
            :50
        ]
        
        return render(
            request, "offers/search.html", {"query": query, "offers": offers}
        )
    else:
        message = ""
        return render(request, "offers/search.html", {"message": message})
"""
def search_categories(request):
    if request.method == "POST":
        query = request.POST["query"]
        categories = Category.objects.filter(name__icontains=query)
     
        #cat = Category.objects.filter(offer__in=offers)
        #all= Offer.objects.filter()
        
        return render(
            request, "offers/search.html", {"query": query, "categories": categories}
        )
    else:
        message = ""
        return render(request, "offers/search.html", {"message": message})
"""
@login_required

def add_comment(request, id):
    """View allowed to add a user's comment in add-comment page and to save it """
    offer = Offer.objects.get(id=id)
    form = CommentForm(instance=offer)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=offer)
        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data["comment_body"]
            comments = Comment(
                offer=offer,
                commenter_name=name,
                comment_body=body,
                date_added=datetime.now(),
                user = request.user,)
            comments.save()
            return redirect("view_offer", offer_id=id)
        else:
            print("form is not valid")
    else:
        form = CommentForm
    context = {"form": form}
    return render(request, "offers/add_comment.html", context)

@login_required
@permission_required('offers.delete_comment', raise_exception=True)
def delete_comment(request, id):
    """View to delete a comment by it's owner"""
    comment = Comment.objects.get(pk=id)
    offer_id= comment.offer_id
    comment.delete()
    return redirect("view_offer", offer_id = offer_id)

def view_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    #offers = Offer.objects.all(id=offer_id)
    return render(request, 'offers/view_category.html', {'category': category})


def view_categories(request):
    categories = Category.objects.all()
    
    return render(request,'offers/view_categories.html', {'categories': categories})

def search_categories(request):
    if request.method == "POST":
        query = request.POST["query"]
        offers = Offer.objects.filter(description__icontains=query).order_by("date_added")
        
        categories = Category.objects.filter(offer__in=offers)
        all = [category.category_id for category in categories]
        alloffers = Offer.objects.filter(id__in=all)
     
        #cat = Category.objects.filter(offer__in=offers)
        #all= Offer.objects.filter()
        
        return render(
            request, "offers/search.html", {"query": query, "alloffers": alloffers}
        )
    else:
        message = ""
        return render(request, "offers/search.html", {"message": message})
