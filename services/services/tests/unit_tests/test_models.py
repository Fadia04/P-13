import pytest

#from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
from users.models import User
from offers.models import Offer, Category, Comment


@pytest.mark.django_db
def test_offer_model():
    """Test the creation of an offer model"""
    cat=Category.objects.create(name="bricolage")
    test_user = User.objects.create_user(username="test_user", password="123456789")
    offer = Offer.objects.create(title="perceuse", description="échange une perceuse", category=cat, user=test_user, type="offre")
    
    expected_value = "perceuse bricolage échange une perceuse offre"
    assert str(offer) == expected_value
    
@pytest.mark.django_db
def test_category_model():
    """Test the creation of a category model"""
    categories = Category.objects.create(name="bricolage")
    expected_value = "bricolage"
    assert str(categories) == expected_value

@pytest.mark.django_db
def test_comment_model():
    """Test the creation of a comment model"""
    cat=Category.objects.create(name="bricolage")
    test_user = User.objects.create_user(username="test_user", password="123456789")
    offer = Offer.objects.create(title="perceuse", description="échange une perceuse", category=cat, user=test_user, type="offre")
    user1=User.objects.create_user(username="user1", password="1234567")
    comment= Comment.objects.create(offer=offer, user=user1, commenter_name="lili")
    expected_value = "perceuse user1 lili"
    assert str(comment) == expected_value