import pytest

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from offers.models import Offer, Category, Comment


@pytest.mark.django_db
def test_offer_model():
    """Test the creation of an offer model"""
    cat=Category.objects.create(category="bricolage")
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
    cat=Category.objects.create(category="bricolage")
    test_user = User.objects.create_user(username="test_user", password="123456789")
    offer = Offer.objects.create(title="perceuse", description="échange une perceuse", category=cat, user=test_user)
    comment= Comment.objects.create(offer, comment_body="blblbl")
    expected_value = "blblbl test_user1"
    assert str(comment) == expected_value