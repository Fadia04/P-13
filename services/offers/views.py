from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from django.shortcuts import get_object_or_404
from datetime import datetime
from itertools import chain
from offers.models import Offer, Category, Comment
from offers.forms import CommentForm

# Create your views here.


def home(request):
    """View dedicated to return home page"""
    return render(request, "offers/home.html")


@login_required
def offer_creation(request):
    """View to display create_offer page and allow the user to create an offer annoucement """
    offer_form = forms.OfferForm()
    if request.method == "POST":
        offer_form = forms.OfferForm(request.POST)
        if offer_form.is_valid():
            offer = offer_form.save(commit=False)
            offer.user = request.user
            offer.type = "Offre"
            offer.save()
            return redirect("home")
    context = {
        "offer_form": offer_form,
    }
    return render(request, "offers/create_offer.html", context=context)


@login_required
def request_creation(request):
    """View to display create_offer page and allow the user to create a request annoucement """
    offer_form = forms.OfferForm()
    if request.method == "POST":
        offer_form = forms.OfferForm(request.POST)
        if offer_form.is_valid():
            offer = offer_form.save(commit=False)
            offer.user = request.user
            offer.type = "Demande"
            offer.save()
            return redirect("home")
    context = {
        "offer_form": offer_form,
    }
    return render(request, "offers/create_request.html", context=context)


@login_required
def modifie_offer(request, offer_id):
    """View to display modifie_offer page and allow the user, when he is logged in,
    to change or delete his own offer and return to home page """
    offer = get_object_or_404(Offer, id=offer_id)
    modifie_form = forms.OfferForm(instance=offer)
    delete_form = forms.DeleteOfferForm()
    if request.method == "POST":
        if offer.user != request.user:
            message = ""
        else:
            if "modifie_offer" in request.POST:
                modifie_form = forms.OfferForm(request.POST, instance=offer)
                if modifie_form.is_valid():
                    modifie_form.save()
                    return redirect("home")
                if "delete_offer" in request.POST:
                    delete_form = forms.DeleteOfferForm(request.POST)
                    if delete_form.is_valid():
                        offer.delete()
                        return redirect("home")
    context = {
        "modifie_form": modifie_form,
        "delete_form": delete_form,
        "message": message
    }
    return render(request, "offers/modifie_offer.html", context=context)


def view_offer(request, offer_id):
    """View to display view_offer page, with all offer informations,
    and to count the number of comments added for this offer """
    offer = get_object_or_404(Offer, id=offer_id)
    num_comments = Comment.objects.filter(offer=offer).count()
    return render(
        request,
        "offers/view_offer.html",
        {"offer": offer, "num_comments": num_comments},
    )


def view_offers(request):
    """View dedicated to display view_offers page and display all
    published annoucements according to their type: offer"""
    offers = Offer.objects.all().filter(type="Offre")
    return render(request, "offers/view_offers.html", {"offers": offers})


def view_myoffers(request):
    """View dedicated to display view_myoffers page and display all offers published by the logged in user"""
    myoffers = Offer.objects.all().filter(user=request.user.id, type="Offre")
    return render(request, "offers/view_myoffers.html", {"myoffers": myoffers})


def view_requests(request):
    """View dedicated to display view_requests page and display all pubished requests"""
    requests = Offer.objects.all().filter(type="Demande")
    return render(request, "offers/view_requests.html", {"requests": requests})


def view_myrequests(request):
    """View dedicated to display view_myoffers page and display all requests published by the logged in user"""
    myrequests = Offer.objects.all().filter(user=request.user.id, type="Demande")
    print(myrequests)
    return render(request, "offers/view_myrequests.html", {"myrequests": myrequests})


def search(request):
    """View allowed to get the user request, when exits, filtered by the type of annoucement,
    thename entered in the query or by the category posted in the query and displays a list of
    corresponding offers in search page"""
    if request.method == "POST":
        query = request.POST["query"]
        type1 = request.POST["type"]
        print(type1)
        offers = Offer.objects.filter(
            description__icontains=query, type=type1
        ).order_by("date_added")[:50]
        cat = Offer.objects.filter(category__name__icontains=query, type=type1)
        results = chain(offers, cat)
        return render(
            request, "offers/search.html", {"query": query, "offers": results}
        )
    else:
        message = ""
        return render(request, "offers/search.html", {"message": message})


@login_required
def add_comment(request, id):
    """View allowed to display add-comment page containig a form 
    allowing the connected user to add his message and to save it and returns view_offer page"""
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
                user=request.user,
            )
            comments.save()
            return redirect("view_offer", offer_id=id)
        else:
            print("form is not valid")
    else:
        form = CommentForm
    context = {"form": form}
    return render(request, "offers/add_comment.html", context)


def view_mycomments(request):
    """View to display view_mycomments page containing all messages published by the logged in user"""
    mycomments = Comment.objects.all().filter(user=request.user.id)
    return render(request, "offers/view_mycomments.html", {"mycomments": mycomments})


@login_required
def delete_comment(request, id):
    """View to delete a message publishe by it's owner"""
    comment = Comment.objects.get(pk=id)
    offer_id = comment.offer_id
    if comment.user == request.user:
        comment.delete()
    else:
        mess = "Vous ne pouvez pas supprimer ce commentaire"
        return render(request, "offers/view_offers.html", {"message": mess})

    return redirect("view_offer", offer_id=offer_id)


def view_category(request, category_id):
    """View used to return view_category page witch display all pubishe offers for the category requested"""
    category = get_object_or_404(Category, id=category_id)
    if category == None:
        offers = Offer.objects.order_by("date_added")
    else:
        offers = Offer.objects.filter(category__name=category)
    return render(
        request, "offers/view_category.html", {"category": category, "offers": offers}
    )


def view_categories(request):
    """View to return view_categories page containing a list of all the publishe categories"""
    categories = Category.objects.all().order_by("name")
    return render(request, "offers/view_categories.html", {"categories": categories})


@login_required
def modifie_comment(request, comment_id):
    """View dedicated to return modifie_comment page allowing the logged in user to modifie his own pubished message"""
    comment = get_object_or_404(Comment, id=comment_id)
    offer_id = comment.offer_id
    modifie_form = forms.CommentForm(instance=comment)

    if request.method == "POST":
        if comment.user != request.user:
            message = ""
        else:
            if "modifie_comment" in request.POST:
                modifie_form = forms.CommentForm(request.POST, instance=comment)
                if modifie_form.is_valid():
                    modifie_form.save()
                    return redirect("view_offer", offer_id=offer_id)

    context = {
        "modifie_form": modifie_form,
    }
    return render(request, "offers/modifie_comment.html", context=context)


def legal_notices(request):
    """View used to return notices page"""
    return render(request, "offers/legal_notices.html")
