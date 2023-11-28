"""services URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
import users.views
import offers.views

urlpatterns = [
    path("admin/", admin.site.urls),
    #path("", TemplateView.as_view(template_name="offers/home.html"), name="home",),
    path("", offers.views.home, name="home"),
    path("users/", include("django.contrib.auth.urls")),
    path("signin/", users.views.login_page, name="signin"),
    path("logout/", users.views.logout_user, name="logout"),
    path("signup/", users.views.signup_page, name="signup"),
    path("create_offer/", offers.views.offer_creation, name="create-offer"),
    path("create_request/", offers.views.request_creation, name="create-request"),
    path('view_offers/', offers.views.view_offers, name='view_offers'),
    path('view_offer/<int:offer_id>', offers.views.view_offer, name='view_offer'),
    path('view_myoffers/', offers.views.view_myoffers, name='view_myoffers'),
    path('view_requests/', offers.views.view_requests, name='view_requests'),
    path('view_myrequests/', offers.views.view_myrequests, name='view_myrequests'),
    path('modifie_offer/<int:offer_id>', offers.views.modifie_offer, name='modifie_offer'),
    path('view_categories/', offers.views.view_categories, name='view_categories'),
    path('view_category/<int:category_id>', offers.views.view_category, name='view_category'),
    path('search/', offers.views.search, name='search'),
    path("offers/<int:id>/add-comment", offers.views.add_comment, name="add-comment"),
    path('view_mycomments/', offers.views.view_mycomments, name='view_mycomments'),
    path('modifie_comment/<int:comment_id>', offers.views.modifie_comment, name='modifie_comment'),   
    path("delete-comment/<int:id>",offers.views.delete_comment,name="delete-comment",),
    
    
   
    #path('search_categories/', offers.views.search_categories, name='search_categories'),
]   

