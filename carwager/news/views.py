from django.shortcuts import render, redirect
import logging

from news.forms import AddNewForm
from news.models import News

logger = logging.getLogger(__name__)


# news page
def news_list_all(request):
    if request.user.is_anonymous:
        return redirect("auth")
    news = News.objects.order_by("-created_at")
    logger.info(f"News list")
    return render(request, "news/news_list.html", {"news": news})


# show current new
def news_view(request, slug):
    news = News.objects.get(slug=slug)
    return render(request, "news/news_view.html", {"news": news})


# create new only for admin
def create_new(request, *args, **kwargs):
    if request.user.is_superuser:
        if request.method == "POST":
            form = AddNewForm(request.POST, request.FILES)
            if form.is_valid():
                logger.info(form.cleaned_data)
                news = News.objects.create(**form.cleaned_data)
                news.save()
            return redirect("news")
        else:
            form = AddNewForm()
            return render(request, "news/create_new.html", {"form": form})
    else:
        return redirect("news")
