from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from . import forms
from django.shortcuts import get_object_or_404
from datetime import datetime
from itertools import chain
from offers.models import Offer, Category, Comment
from offers.forms import OfferForm, CommentForm
from django.db.models import Q
# Create your views here.

def home(request):
    """View allowed to return home page"""
    return render(request, "offers/home.html")

@login_required
def offer_creation(request):
    offer_form = forms.OfferForm()
    if request.method == 'POST':
        offer_form = forms.OfferForm(request.POST)
    
        if offer_form.is_valid():
            offer = offer_form.save(commit=False)
            offer.user = request.user
            offer.type = 'Offre'
            offer.save()
            return redirect('home')
            
    context = {
        'offer_form': offer_form,
        
}
    return render(request, 'offers/create_offer.html', context=context)

@login_required
def request_creation(request):
    offer_form = forms.OfferForm()
    if request.method == 'POST':
        offer_form = forms.OfferForm(request.POST)
    
        if offer_form.is_valid():
            offer = offer_form.save(commit=False)
            offer.user = request.user
            offer.type = 'Demande'
            offer.save()
            return redirect('home')
            
    context = {
        'offer_form': offer_form,
        
}
    return render(request, 'offers/create_request.html', context=context)

@login_required
#@permission_required('offers.modifie_offer', raise_exception=True)
def modifie_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    modifie_form = forms.OfferForm(instance=offer)
    delete_form = forms.DeleteOfferForm()
    
    if request.method == 'POST':
        if offer.user!= request.user:
            message= ""
        else:
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
    num_comments = Comment.objects.filter(offer=offer).count()
        
    #offers = Offer.objects.all(id=offer_id)
    return render(request, 'offers/view_offer.html', {'offer': offer,'num_comments':num_comments})


def view_offers(request):
    #offers = Offer.objects.all()
    offers = Offer.objects.all().filter(type='Offre')
       
    return render(request,'offers/view_offers.html', {'offers': offers})

def view_myoffers(request):
    #offers = Offer.objects.all()
    myoffers = Offer.objects.all().filter(user=request.user, type = 'Offre')
       
    return render(request,'offers/view_myoffers.html', {'myoffers': myoffers})

def view_requests(request):
    #requests = Offer.objects.all()
    requests = Offer.objects.all().filter(type='Demande')
       
    return render(request,'offers/view_requests.html', {'requests': requests})

def view_myrequests(request):
    #offers = Offer.objects.all()
    myrequests = Offer.objects.all().filter(user=request.user, type = 'Demande')
    print(myrequests)  
    return render(request,'offers/view_myrequests.html', {'myrequests': myrequests})


def search(request):
    if request.method == "POST":
        query = request.POST["query"]
        type1 = request.POST["type"]
        print(type1)
        offers = Offer.objects.filter(description__icontains=query, type=type1).order_by("date_added")[:50]
        #offers = Offer.objects.filter(Q(description__icontains=query), Q(type='Offre') | Q(type='Demande'),)
        cat = Offer.objects.filter(category__name__icontains=query, type=type1)
        results = chain(offers, cat)
        return render(
            request, "offers/search.html", {"query": query, "offers":results}
        )
    else:
        message = ""
        return render(request, "offers/search.html", {"message": message})
"""
def search_categories(request):
    if request.method == "POST":
        query = request.POST["query"]
        offers = Offer.objects.filter(category__name__icontains=query)
     
        
        return render(
            request, "offers/search.html", {"query": query, "offers": offers}
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

def view_mycomments(request):
    #offer = get_object_or_404(Offer, id=offer_id )
    mycomments = Comment.objects.all().filter(user=request.user)
    #user = Comment.objects.filter(offer=offer_id)
    print(mycomments)
       
    return render(request,'offers/view_mycomments.html', {'mycomments': mycomments})


@login_required
#@permission_required('offers.delete_comment', raise_exception=True)
def delete_comment(request, id):
    """View to delete a comment by it's owner"""
    comment = Comment.objects.get(pk=id)
    offer_id = comment.offer_id
    if comment.user == request.user:
        comment.delete()
    else:
        mess="Vous ne pouvez pas supprimer ce commentaire"
        return render(request,"offers/view_offers.html", {'message':mess})
        #return redirect("view_offers")
    return redirect("view_offer", offer_id = offer_id)
    #return redirect("view_offers")
    
    
#def show_comment(request):
    #"""View to read a comment by it's owner"""
    #comment = Comment.objects.filter(user = request.user)
    #comment = Comment.objects.filter(user = comment.user.username)    
    #return render("offers/add_comment.html", comment)


"""
def view_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    return render(request, 'offers/view_category.html', {'category': category})

"""
def view_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if category == None:
        offers = Offer.objects.order_by("date_added")
    else:
        offers = Offer.objects.filter(category__name=category)
    return render(request, 'offers/view_category.html', {'category': category, 'offers': offers})

def view_categories(request):
    categories = Category.objects.all()
    
    return render(request,'offers/view_categories.html', {'categories': categories})



@login_required
#@permission_required('offers.modifie_offer', raise_exception=True)
def modifie_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    offer_id = comment.offer_id
    modifie_form = forms.CommentForm(instance=comment)
    #delete_form = forms.DeleteOfferForm()
    
    if request.method == 'POST':
        if comment.user!= request.user:
            message= ""
        else:
            if 'modifie_comment' in request.POST:
                modifie_form = forms.CommentForm(request.POST, instance=comment)
                if modifie_form.is_valid():
                    modifie_form.save()
                    return redirect('view_offer', offer_id = offer_id)
                
                #if 'delete_offer' in request.POST:
                    #delete_form = forms.DeleteOfferForm(request.POST)
                    #if delete_form.is_valid():
                        #offer.delete()
                        #return redirect('home')
    
    context = {
        'modifie_form': modifie_form,
        #'delete_form': delete_form,
}
    return render(request, 'offers/modifie_comment.html', context=context)


"""
def view_type(request):
    types = Offer.objects.all.filter(type='Demande').filter(type='Offres')
    
    return render(request,'offers/view_categories.html', {'types': types})
"""

"""
def search_categories(request):
    if request.method == "POST":
        query = request.POST["query"]
        offers = Offer.objects.filter(description__icontains=query).order_by("date_added")
        
        categories = Category.objects.filter(name__in=offers)
        cat_id = [category.category_id for category in categories]
        offer_id = Offer.objects.filter(category_id__in=cat_id)
     
        #cat = Category.objects.filter(offer__in=offers)
        #all= Offer.objects.filter()
        
        return render(
            request, "offers/search.html", {"query": query, "category": alloffers}
        )
    else:
        message = ""
        return render(request, "offers/search.html", {"message": message})
"""