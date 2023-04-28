from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from django.shortcuts import get_object_or_404
from offers.models import Offer, Category
from offers.forms import OfferForm
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

@login_required
def view_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    #offers = Offer.objects.all(id=offer_id)
    return render(request, 'offers/view_offer.html', {'offer': offer})

@login_required
def view_offers(request):
    offers = Offer.objects.all()
    
    return render(request,'offers/view_offers.html', {'offers': offers})


def search(request):
    if request.method == "POST":
        query = request.POST["query"]
        offers = Offer.objects.filter(title__icontains=query).order_by("date_added")[
            :50
        ]
        print(offers)
        
        

        return render(
            request, "offers/search.html", {"query": query, "offers": offers}
        )
    else:
        message = "Nous n'avons pas trouvé l'annonce recherchée, veuillez retaper votre demande"
        return render(request, "offers/search.html", {"message": message})
