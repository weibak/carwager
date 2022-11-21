"""general URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from auction.views import CarAuctionView, auction_view, create_auction
from general.views import register, sign_in, logout_view, profile_view
from news.views import news_list_all, news_view
from showbill.views import CarView, create_advert, advert_view

urlpatterns = [
    path("admin/django-rq/", include("django_rq.urls")),
    path('admin/', admin.site.urls),
    path("api/", include("api.urls", namespace="api")),
    path('', CarView.as_view(), name="home"),
    path("register/", register, name="register"),
    path("auth/", sign_in, name="auth"),
    path("logout/", logout_view, name="logout"),
    path('showbill/', CarView.as_view(), name="showbill"),
    path('news/', news_list_all, name="news"),
    path('news/<str:slug>/', news_view, name="news_view"),
    path('profile/', profile_view, name="profile"),
    path("advert/<int:advert_id>", advert_view, name="car_details"),
    path('showbill/add/', create_advert, name="add_advert"),
    path('auction/', CarAuctionView.as_view(), name="auction"),
    path("details/<int:auction_id>/", auction_view, name="auction_details"),
    path('auction/add/', create_auction, name="add_auction"),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
