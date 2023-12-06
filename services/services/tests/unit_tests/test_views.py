import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from django.test import Client
from offers.models import Offer, Category, Comment
from users.models import User
#from django.contrib.auth.models import User


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
    User.objects.create(username="test_user", password="123456789")
    path = reverse("signin")
    response = client.post(path, {"username": "test_user", "password": "123456789"})
    assert response.status_code == 200
    assertTemplateUsed(response, "users/signin.html")
    
@pytest.mark.django_db
def test_logout_page_view():
    client = Client()
    path = reverse("logout")
    response = client.get(path)
    assert response.status_code == 302
    assert response.url == "/signin/"
    
@pytest.mark.django_db
def test_signup_page_view():
    client = Client()
    test_user = {
        "first_name": "Loulou",
        "last_name": "lili",
        "username": "test",
        "password1": "nanou1234",
        "password2": "nanou1234",
    }
    path = reverse("signup")
    response = client.post(path, test_user)
    assert response.status_code == 302
    #assertTemplateUsed(response, "users/signup.html")
    assert response.url == "/"
    
@pytest.mark.django_db
def test_add_comment_view():
    client = Client()
    test_user=User.objects.create(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat, user=test_user, type="demande")
    User.objects.create(username="Lamia", password="lili5678")
    client.login(username="Lamia", password="lili5678")
    path = reverse("add-comment", kwargs={"id": offer.id})
    #data = {"comment_body": "CommentTextMessageTest", "username": "Lamia" , "password": "lili5678" }
    response = client.post(path)
    assert response.status_code == 302
    #assertTemplateUsed(response,"offers/add_comment.html")
    
@pytest.mark.django_db
def test_create_offer_view():
    client = Client()
    
    path = reverse("create-offer")
    response = client.post(path)
    

    assert response.status_code == 302
    assertTemplateUsed(response,"offers/offers.html")
    
@pytest.mark.django_db
def view_offer_view():
    client = Client()
    test_user=User.objects.create(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat, user=test_user, type="offre")
    User.objects.create(username="Lamia", password="lili5678")
    client.login(username="Lamia", password="lili5678")
    path = reverse("view_offer", kwargs={"id": offer.id})
    #data = {"comment_body": "CommentTextMessageTest", "username": "Lamia" , "password": "lili5678" }
    response = client.get(path)
    content = response.content.decode()
    expected_content = "perceuse échange perceuse bricolage offre"
    assert content == expected_content
    assert response.status_code == 200
    assertTemplateUsed(response,"offers/view_offer.html")
    
@pytest.mark.django_db
def view_request_view():
    client = Client()
    test_user=User.objects.create(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat, user=test_user, type="demande")
    User.objects.create(username="Lamia", password="lili5678")
    client.login(username="Lamia", password="lili5678")
    path = reverse("view_request", kwargs={"id": offer.id})
    #data = {"comment_body": "CommentTextMessageTest", "username": "Lamia" , "password": "lili5678" }
    response = client.get(path)
    content = response.content.decode()
    expected_content = "perceuse échange perceuse bricolage demande"
    assert content == expected_content
    assert response.status_code == 200
    assertTemplateUsed(response,"offers/view_request.html")
    
@pytest.mark.django_db
def view_requests_view():
    client = Client()
    test_user=User.objects.create(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat, user=test_user, type="demande")
    User.objects.create(username="Lamia", password="lili5678")
    client.login(username="Lamia", password="lili5678")
    path = reverse("view_offers")
    response = client.get(path)
    content = response.content.decode()
    expected_content = "perceuse bricolage"
    assert content == expected_content
    assert response.status_code == 200
    assertTemplateUsed(response,"offers/view_offers.html")
    
@pytest.mark.django_db
def view_offers_view():
    client = Client()
    test_user=User.objects.create(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat, user=test_user, type="offre")
    #User.objects.create(username="test_user", password="5678")
    client.login(username="test_user", password="5678")
    path = reverse("view_offers")
    response = client.get(path)
    content = response.content.decode()
    expected_content = "perceuse bricolage échange"
    assert content == expected_content
    assert "perceuse" in content
    assert response.status_code == 200
    assertTemplateUsed(response,"offers/view_offers.html")
    
@pytest.mark.django_db
def view_categories_view():
    client = Client()
    categories = Category.objects.create(name1="bricolage", name2= "pet_sitting")
    #category2=
    path = reverse("view_categories")
    response = client.get(path)
    content = response.content.decode()
    expected_content = "bricolage pet_sitting"
    assert content == expected_content
    assert response.status_code == 200
    assertTemplateUsed(response,"offers/view_categories.html")
    
    
@pytest.mark.django_db
def view_category_view():
    client = Client()
    category = Category.objects.create(name="bricolage")
    path = reverse("view_category", kwargs={category.id: "id"})
    response = client.get(path)
    content = response.content.decode()
    expected_content = "bricolage"
    assert content == expected_content
    assert response.status_code == 200
    assertTemplateUsed(response,"offers/view_category.html")
    
@pytest.mark.django_db
def search_view():
    client = Client()
    test_user=User.objects.create(username="test_user", password="5678")
    cat1 = Category.objects.create(name="bricolage")
    cat2 = Category.objects.create(name="cours")
    offer1 = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat1, user=test_user, type="offre")
    offer2 = Offer.objects.create(title="marteau", description = "prète un marteau", category=cat2, user=test_user, type="offre")
    User.objects.create(username="Lamia", password="lili5678")
    client.login(username="Lamia", password="lili5678")
    path = reverse("search")
    response = client.post(path, {"query": "perceuse"})
    content = response.content.decode()
    expected_content = "perceuse échange une perceuse bricolage offre"
    assert content == expected_content
    assert response.status_code == 200
    assertTemplateUsed(response,"offers/search.html")
    