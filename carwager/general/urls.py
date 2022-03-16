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
from django.urls import path

from general.views import register, sign_in, logout_view
from news.views import news_list_all
from showbill.views import CarView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CarView.as_view(), name="home"),
    path("register/", register, name="register"),
    path("auth/", sign_in, name="auth"),
    path("logout/", logout_view, name="logout"),
    path('showbill/', CarView.as_view(), name="news"),
   # path('showbill/', "admin.site.urls", name="showbill"),
   # path('cars/', "admin.site.urls", name="cars"),
   # path('cars/auction/', "admin.site.urls", name="cars_auction"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
