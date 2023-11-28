import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from django.test import Client
from offers.models import Offer, Category, Comment
from django.contrib.auth.models import User


def test_home_view():
    client = Client()
    client.post("/")
    path = reverse("home")
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "offers/home.html")


@pytest.mark.django_db
def test_login_page_view():
    client = Client()
    User.objects.create_user(username="test_user", password="123456789")
    path = reverse("login")
    response = client.post(path, {"username": "test_user", "password": "123456789"})
    assert response.status_code == 302
    assert response.url == "/"
    
@pytest.mark.django_db
def test_add_comment_view():
    client = Client()
    cat = Category.objects.create(category="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat)
    User.objects.create_user(username="Lamia", password="lili5678")
    client.login(username="Lamia", password="lili5678")
    path = reverse("add-comment", kwargs={"id": offer.id})
    data = {"comment_body": "CommentTextMessageTest"}
    response = client.post(path, data)
    assert response.status_code == 302
    path = reverse("view_offer", kwargs={"id": offer.id})
    assert response.url == path
    
@pytest.mark.django_db
def test_search_view():
    client = Client()
    offer1 = Offer.objects.create(title="perceuse", id="")
    offer2 = Offer.objects.create(title="raclette", id="2")
    offer3 = Offer.objects.create(title="chaton", id="3")
    category1 = Category.objects.create(name="bricolage")
    category2 = Category.objects.create(name="pet-sitting")

    
    path = reverse("search")
    response = client.post(path, {"query": "perceuse"})
    assert response.status_code == 200
    assertTemplateUsed(response, "offers/search.html")
    