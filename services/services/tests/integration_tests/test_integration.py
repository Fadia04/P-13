import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed
from offers.models import Offer, Category
from django.contrib import auth


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
    path = reverse("view_offers")
    test_user = User.objects.create(username="test", password="5678")
    cat1 = Category.objects.create(name="bricolage")
    cat2 = Category.objects.create(name="cours")
    Offer.objects.create(title="perceuse", description="échange une perceuse",
                         category=cat1, user=test_user, type="Offre")
    Offer.objects.create(title="maths", description="donne cours de maths",
                         category=cat2, user=test_user, type="Offre")
    response = client.get(path)
    content = response.content.decode()
    expected_content = "perceuse"
    assert expected_content in content
    assert response.status_code == 200
    assertTemplateUsed(response, "offers/view_offers.html")


@pytest.mark.django_db
def test_integration_login_search():
    client = Client()
    User.objects.create_user(username="test_user", password="123456789")
    path = reverse("signin")
    response = client.post(path, {"username": "test_user", "password": "123456789"})
    path = reverse("search")
    test_user = User.objects.create(username="test", password="5678")
    cat1 = Category.objects.create(name="bricolage")
    cat2 = Category.objects.create(name="cours")
    Offer.objects.create(title="perceuse", description="échange une perceuse",
                         category=cat1, user=test_user, type="Offre")
    Offer.objects.create(title="maths", description="donne cours de maths",
                         category=cat2, user=test_user, type="Offre")
    response = client.post(path, {"query": "maths", "type": "offre"})
    content = response.content.decode()
    expected_content = "maths"
    assert expected_content in content
    assert response.status_code == 200
    assertTemplateUsed(response, "offers/search.html")


@pytest.mark.django_db
def test_integration_login_create_offer():
    client = Client()
    User.objects.create_user(username="test_user", password="123456789")
    path = reverse("signin")
    response = client.post(path, {"username": "test_user", "password": "123456789"})
    path = reverse("create-offer")
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "offers/create_offer.html")


@pytest.mark.django_db
def test_integration_search_view_offer():
    client = Client()
    test_user = User.objects.create(username="test", password="5678")
    cat1 = Category.objects.create(name="bricolage")
    cat2 = Category.objects.create(name="cours")
    Offer.objects.create(title="perceuse", description="échange une perceuse",
                         category=cat1, user=test_user, type="Offre")
    offer = Offer.objects.create(title="maths", description="donne cours de maths",
                                 category=cat2, user=test_user, type="Offre")
    path = reverse("search")
    response = client.post(path, {"query": "maths", "type": "offre"})
    path = reverse("view_offer", kwargs={"offer_id": offer.id})
    response = client.get(path)
    content = response.content.decode()
    expected_content = 'maths'
    assert expected_content in content
    assert response.status_code == 200
    assertTemplateUsed(response, "offers/view_offer.html")
