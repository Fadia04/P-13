import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertRedirects, assertContains
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
    User.objects.create_user(username="test_user", password="123456789")
    path = reverse("signin")
    response = client.get(path, {"username": "test_user", "password": "123456789"})
    assert response.status_code == 200
    assertTemplateUsed(response, "users/signin.html")
    
@pytest.mark.django_db
def test_login_page_success_redirect_to_home_view():
    client = Client()
    User.objects.create_user(username="test_user", password="123456789")
    
    path = reverse("signin")
    response = client.post(path, {"username": "test_user", "password": "123456789"})
    assertRedirects(
        response=response, expected_url="/", status_code=302, target_status_code=200
    )
    
@pytest.mark.django_db
def test_logout_page_view():
    client = Client()
    path = reverse("logout")
    response = client.get(path)
    assert response.status_code == 302
    assert response.url == "/signin/"
    
@pytest.mark.django_db
def test_signup_page_success_redirect_to_home_view():
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
    #assert response.url == "/"
    assertRedirects(
        response=response, expected_url="/", status_code=302, target_status_code=200
    )
    

    

@pytest.mark.django_db
def test_create_offer_view():
    client = Client()
    User.objects.create_user(username="Lamia", password="lili5678")
    client.login(username="Lamia", password="lili5678")    
    path = reverse("create-offer")
    response = client.get(path)    
    assert response.status_code == 200
    assertTemplateUsed(response,"offers/create_offer.html")

@pytest.mark.django_db
def test_create_offer_success_is_redirected_to_home_view():
    client = Client()
    User.objects.create_user(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    
    client.login(username="test_user", password="5678")    
    data = {"title": "perceuse", "description":"échange une perceuse", "category":cat, "available": True, "modifie_offer": True}
    path = reverse("create-offer")
    response = client.post(path, data, follow=True)
    
    assertRedirects(
        response=response,
        expected_url="/",
        status_code=302,
        target_status_code=200,)
    assertTemplateUsed(response, "offers/home.html")
    
@pytest.mark.django_db
def test_view_offer_view():
    client = Client()
    test_user=User.objects.create_user(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat, user=test_user, type="Offre")
    User.objects.create_user(username="Lamia", password="lili5678")
    client.login(username="Lamia", password="lili5678")
    path = reverse("view_offer", kwargs={"offer_id": offer.id})
    
    response = client.get(path)
    content = response.content.decode()
    #expected_content = "perceuse échange perceuse bricolage"
    #assert content == expected_content
    assert response.status_code == 200
    assertContains(response, "perceuse")
    assertTemplateUsed(response,"offers/view_offer.html")
    
@pytest.mark.django_db
def test_modifie_offer_view():
    client = Client()
    test_user=User.objects.create_user(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat, user=test_user, type="Offre")
    User.objects.create_user(username="Lamia", password="lili5678")
    client.login(username="Lamia", password="lili5678")
    path = reverse("modifie_offer", kwargs={"offer_id": offer.id})
    response = client.post(path)
    content = response.content.decode()
    #expected_content = "perceuse échange perceuse bricolage"
    #assert content == expected_content
    assert response.status_code == 200
    assertContains(response, "perceuse")
    assertTemplateUsed(response,"offers/modifie_offer.html")
 
@pytest.mark.django_db    
def test_modifie_offer_is_redirected_successfully():
    client = Client()
    test_user=User.objects.create_user(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat, user=test_user, type="Offre")
    
    client.login(username="test_user", password="5678")
    data = {"title": "perceuse", "description":"échange une perceuse", "category":cat, "available":True, "modifie_offer": True}
    path = reverse("modifie_offer", kwargs={"offer_id": offer.id})
    response = client.post(path, data, follow=True)
    assertRedirects(
        response=response,
        expected_url="/",
        status_code=302,
        target_status_code=200,)
    assertTemplateUsed(response, "offers/home.html")
    
    
@pytest.mark.django_db
def test_view_request_view():
    client = Client()
    test_user=User.objects.create_user(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat, user=test_user, type="Demande")
    User.objects.create_user(username="Lamia", password="lili5678")
    client.login(username="Lamia", password="lili5678")
    path = reverse("view_offer", kwargs={"offer_id": offer.id})
    #data = {"comment_body": "CommentTextMessageTest", "username": "Lamia" , "password": "lili5678" }
    response = client.get(path)
    content = response.content.decode()
    #expected_content = "échange perceuse bricolage demande"
    #assert content == expected_content
    assertContains(response, "perceuse")
    assert response.status_code == 200    
    assertTemplateUsed(response,"offers/view_offer.html")
    
@pytest.mark.django_db
def test_view_offers_view():
    client = Client()
    test_user=User.objects.create_user(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat, user=test_user, type="Offre")
    offer2= Offer.objects.create(title="maths", description = "donne cours de maths", category=cat, user=test_user, type="Offre")
    User.objects.create_user(username="test", password="678")
    client.login(username="test", password="678")
    path = reverse("view_offers")
    response = client.get(path)
    content = response.content.decode()
    #expected_content = "perceuse bricolage échange"
    #assert content == expected_content
    assert "perceuse" in content
    assert "maths" in content
    assert response.status_code == 200
    assertTemplateUsed(response,"offers/view_offers.html")
    #assertContains(response, "perceuse")
    
@pytest.mark.django_db
def test_view_myoffers_view():
    client = Client()
    test_user=User.objects.create_user(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat, user=test_user, type="Offre")
    offer2= Offer.objects.create(title="maths", description = "donne cours de maths", category=cat, user=test_user, type="Offre")
    
    client.login(username="test_user", password="5678")
    path = reverse("view_myoffers")
    response = client.get(path)
    content = response.content.decode()
    #expected_content = "perceuse bricolage échange"
    #assert content == expected_content
    assert "perceuse" in content
    assert "maths" in content
    assert response.status_code == 200
    assertTemplateUsed(response,"offers/view_myoffers.html")
    #assertContains(response, "perceuse")
    
@pytest.mark.django_db
def test_view_requests_view():
    client = Client()
    test_user=User.objects.create_user(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat, user=test_user, type="Demande")
    #User.objects.create(username="Lamia", password="lili5678")
    client.login(username="test_user", password="5678")
    path = reverse("view_requests")
    response = client.get(path)
    content = response.content.decode()
    #expected_content = "perceuse bricolage"
    #assert content == expected_content
    assert "perceuse" in content
    assert response.status_code == 200
    assertTemplateUsed(response,"offers/view_requests.html")
    
@pytest.mark.django_db
def test_view_myrequests_view():
    client = Client()
    test_user=User.objects.create_user(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat, user=test_user, type="Demande")
    offer2= Offer.objects.create(title="maths", description = "donne cours de maths", category=cat, user=test_user, type="Demande")
    
    client.login(username="test_user", password="5678")
    path = reverse("view_myrequests")
    response = client.get(path)
    content = response.content.decode()
    #expected_content = "perceuse bricolage échange"
    #assert content == expected_content
    assert "perceuse" in content
    assert "maths" in content
    assert response.status_code == 200
    assertTemplateUsed(response,"offers/view_myrequests.html")
    #assertContains(response, "perceuse")
    
@pytest.mark.django_db
def test_view_categories_view():
    client = Client()
    categories = Category.objects.create(name="Bricolage")
    #category2=
    path = reverse("view_categories")
    response = client.get(path)
    content = response.content.decode()
    expected_content = "Bricolage"
    assert expected_content in content
    assert response.status_code == 200
    assertTemplateUsed(response,"offers/view_categories.html")
    assert "Bricolage" in content
    
@pytest.mark.django_db
def test_view_category_view():
    client = Client()
    category = Category.objects.create(name="Bricolage")
    cat2 = Category.objects.create(name="cours")
    test_user=User.objects.create_user(username="test_user", password="5678")
    offer1 = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=category, user=test_user, type="Offre")
    offer2 = Offer.objects.create(title="maths", description = "donne cours de maths", category=cat2, user=test_user, type="Offre")
    path = reverse("view_category", kwargs={"category_id": category.id})
    response = client.get(path)
    content = response.content.decode()
    expected_content = "perceuse"
    assert expected_content in content
    assert response.status_code == 200
    assertTemplateUsed(response,"offers/view_category.html")
    #assert "perceuse maths" in content
    
@pytest.mark.django_db
def test_search_view():
    client = Client()
    test_user=User.objects.create_user(username="test_user", password="5678")
    cat1 = Category.objects.create(name="bricolage")
    cat2 = Category.objects.create(name="cours")
    offer1 = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat1, user=test_user, type="Offre")
    offer2 = Offer.objects.create(title="maths", description = "donne cours de maths", category=cat2, user=test_user, type="Offre")
    #User.objects.create(username="Lamia", password="lili5678")
    #client.login(username="Lamia", password="lili5678")
    path = reverse("search")
    response = client.post(path, {"query": "maths", "type": "offre"})
    content = response.content.decode()
    expected_content = "maths"
    assert expected_content in content
    assert response.status_code == 200
    assertTemplateUsed(response,"offers/search.html")
    #assert response.context["offers"][0]==offer2
    #assert response.context["offers"][1]==offer1
    
    
@pytest.mark.django_db
def test_add_valid_comment_is_redirected_succesfully():
    client = Client()
    test_user=User.objects.create_user(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat, user=test_user, type="Offre")
    User.objects.create_user(username="Lamia", password="lili5678")
    client.login(username="Lamia", password="lili5678")   
    path = reverse("add-comment", kwargs={"id": offer.id})
    data = {"comment_body": "CommentTextMessageTest", "modifie_comment": "True"}
    response= client.post(path, data, follow=True)
    assertRedirects(
        response=response,
        expected_url="/view_offer/id",
        status_code=302,
        target_status_code=200,
    )
    assertTemplateUsed(response, "offers/view_offer.html")
    
@pytest.mark.django_db
def test_view_mycomment_is_valid():
    client = Client()
    test_user=User.objects.create_user(username="test_user", password="5678")
    cat = Category.objects.create(name="bricolage")
    offer = Offer.objects.create(title="perceuse", description = "échange une perceuse", category=cat, user=test_user, type="offre")
    user=User.objects.create_user(username="Lamia", password="lili5678")
    comment = Comment.objects.create(offer=offer, user=user, commenter_name="premier commentaire")
    client.login(username="Lamia", password="lili5678")
    path = reverse("view_mycomments")
    #data = {"comment_body": "CommentTextMessageTest", "modifie_comment": "True"}
    response = client.get(path)
    assert response.status_code == 200
    content = response.content.decode()
    expected_content = "Lamia"
    assert expected_content in content
   
    assertTemplateUsed(response, "offers/view_mycomments.html")
    
