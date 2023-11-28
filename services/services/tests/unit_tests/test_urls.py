import pytest
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from offers.models import Offer, Category, Comment
User=get_user_model()


def test_home_url():
    """Test the home url"""
    path = reverse("home")
    assert path == "/"
    assert resolve(path).view_name == "home"

def test_login_page_url():
    """Test the login url"""
    path = reverse("signin")
    assert path == "/signin/"
    assert resolve(path).view_name == "signin"


def test_logout_user_url():
    """Test the logout url"""
    path = reverse("logout")
    assert path == "/logout/"
    assert resolve(path).view_name == "logout"

def test_signup_page_url():
    """Test the signup url"""
    path = reverse("signup")
    assert path == "/signup/"
    assert resolve(path).view_name == "signup"
    
@pytest.mark.django_db
def test_offer_creation_url():
    """Test the view_offer_creation url"""
    path = reverse("create-offer")
    assert path == "/create_offer/"
    assert resolve(path).view_name == "create-offer"

@pytest.mark.django_db
def test_request_creation_url():
    """Test the view_request_creation url"""
    path = reverse("create-request")
    assert path == "/create_request/"
    assert resolve(path).view_name == "create-request"


@pytest.mark.django_db
def test_search_url():
    """test the search url"""
    path = reverse("search")
    assert path == "/search/"
    assert resolve(path).view_name == "search"
    


@pytest.mark.django_db
def test_view_offers_url():
    """Test the view_offers url"""
    path = reverse("view_offers")
    assert path == "/view_offers/"
    assert resolve(path).view_name == "view_offers"
    
@pytest.mark.django_db
def test_view_offer_url():
    """Test the view_offer url"""
    #offre = Offer.objects.create(title="perceuse", description = "échange une perceuse à percussion")
    cat=Category.objects.create(name="bricolage")
    #model = get_user_model()
    user=User.objects.create(username="test_user", password="1234")
    Offer.objects.create(title="perceuse", description = "échange une perceuse à percussion", category = cat, user=user)
    #Offer.objects.create(offer=offre, category=cat, user=test_user)
    
    path = reverse("view_offer", kwargs={"id": 1})
    assert path == "/offers/1/"
    assert resolve(path).view_name == "view_offer"
    
#@pytest.mark.django_db
#def test_modifie_offer_url():
    
@pytest.mark.django_db
def test_view_my_offers_url():
    """Test the view_my_offers url"""
    path = reverse("view_myoffers")
    assert path == "/view_myoffers/"
    assert resolve(path).view_name == "view_myoffers"
    
@pytest.mark.django_db
def test_view_requests_url():
    """Test the view_requests url"""
    path = reverse("view_requests")
    assert path == "/view_requests/"
    assert resolve(path).view_name == "view_requests"


@pytest.mark.django_db
def test_view_my_requests_url():
    """Test the view_my_requests url"""
    path = reverse("view_myrequests")
    assert path == "/view_myrequests/"
    assert resolve(path).view_name == "view_myrequests"
    
@pytest.mark.django_db
def test_view_categories_url():
    """Test the view_categories url"""
    path = reverse("view_categories")
    assert path == "/view_categories/"
    assert resolve(path).view_name == "view_categories"
    
#@pytest.mark.django_db
#def test_view_category_url():

@pytest.mark.django_db
def test_add_comment_url():
    """Test the add_comment url"""
    cat=Category.objects.create(category="bricolage")
    user = User.objects.create_user(username="user")
    offre = Offer.objects.create(title = "perceuse", description="échange une perceuse", category=cat, user=user)
    #user_1= User.objects.create_user(username="user1")
    Comment.objects.create(offer=offre)
    path = reverse("add-comment", kwargs={"id": 1})
    assert path == "/offers/1/"
    assert resolve(path).view_name == "add-comment"
    
@pytest.mark.django_db
def test_delete_comment_url():
    """Test the delete_comment url"""
    Offer.objects.create(title="perceuse")
    user=User.objects.create_user(username="user1")
    Comment.objects.create(offer=offre, user=user)
    path = reverse("delete-comment", kwargs={"id": 1})
    assert path == "/offers/1/delete-comment"
    assert resolve(path).view_name == "delete-comment"
    
@pytest.mark.django_db
def test_modifie_comment_url():
    """Test the modifie_comment url"""
    Offer.objects.create(title="perceuse")
    path = reverse("modifie_comment", kwargs={"id": 1})
    assert path == "/offers/1/modifie_comment"
    assert resolve(path).view_name == "modifie_comment"