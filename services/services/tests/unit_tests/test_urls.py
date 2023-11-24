import pytest
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from offers.models import Offer
from offers.models import Comment
from offers.models import Category


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
def test_add_comment_url():
    """Test the add_comment url"""
    Offer.objects.create(title = "perceuse")
    path = reverse("add-comment", kwargs={"id": 1})
    assert path == "/offers/1/add-comment"
    assert resolve(path).view_name == "add-comment"


@pytest.mark.django_db
def test_delete_comment_url():
    """Test the delete_comment url"""
    Offer.objects.create(title="perceuse")
    path = reverse("delete-comment", kwargs={"id": 1})
    assert path == "/offers/1/delete-comment"
    assert resolve(path).view_name == "delete-comment"

@pytest.mark.django_db
def test_search_url():
    """test the search url"""
    path = reverse("search")
    assert path == "/search/"
    assert resolve(path).view_name == "search"
    
@pytest.mark.django_db
def test_view_offer_url():
    """Test the view_offer url"""
    Offer.objects.create(title="perceuse")
    path = reverse("view_offer", kwargs={"id": 1})
    assert path == "/offers/1/"
    assert resolve(path).view_name == "view_offer"

@pytest.mark.django_db
def test_view_offers_url():
    """Test the view_offers url"""
    path = reverse("view_offers")
    assert path == "/view_offers/"
    assert resolve(path).view_name == "view_offers"

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
def test_view_my_offers_url():
    """Test the view_my_offers url"""
    path = reverse("view_myoffers")
    assert path == "/view_myoffers/"
    assert resolve(path).view_name == "view_myoffers"

@pytest.mark.django_db
def test_view_my_requests_url():
    """Test the view_my_requests url"""
    path = reverse("view_myrequests")
    assert path == "/view_myrequests/"
    assert resolve(path).view_name == "view_myrequests"
