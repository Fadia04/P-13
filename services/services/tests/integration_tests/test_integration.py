import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed
from django.contrib.auth import get_user_model
from offers.models import Offer, Category, Comment
from users.models import User
from django.contrib import auth
from django.contrib.auth.views import LoginView
User=get_user_model()


@pytest.mark.django_db
def test_integration_signup_login():
    client = Client()
    response = client.post(
        reverse("signup"),
        {
            "first_name": "Loulou",
            "last_name": "lili",
            "username": "test",
            "password1": "nanou1234",
            "password2": "nanou1234",
        },
    )
    path = reverse("signin")
    response = client.post(path, {"username": "test", "password": "nanou1234"})
    assert response.status_code == 302
    assert response.url == "/"
    user = auth.get_user(client)
    assert user.is_authenticated
    
@pytest.mark.django_db
def test_integration_login_logout():
    client = Client()
    User.objects.create_user(username="test_user", password="123456789")
    path = reverse("signin")
    response = client.post(path, {"username": "test_user", "password": "123456789"})
    assert response.status_code == 302
    assert response.url == "/"
    path = reverse("logout")
    response = client.get(path)
    assert response.status_code == 302
    assert response.url == "/signin/"
    
@pytest.mark.django_db
def test_integration_login_view_offers():
    client = Client()
    User.objects.create_user(username="test_user", password="123456789")
    path = reverse("signin")
    response = client.post(path, {"username": "test_user", "password": "123456789"})
    
    #test_user=User.objects.create(username="testuser", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", user="test_user", category=cat, type="demande" )
    path = reverse("view_offers")
    response = client.get(path)
    content = response.content.decode()
    expected_content = "perceuse bricolage"
    assert content == expected_content
    assert response.status_code == 200
    assertTemplateUsed(response, "offers/view_offers.html")
    
   