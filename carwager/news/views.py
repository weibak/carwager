from django.shortcuts import render, redirect
import logging

from news.models import News


logger = logging.getLogger(__name__)


def news_list_all(request):
    if request.user.is_anonymous:
        return redirect("auth")
    news = News.objects.order_by("-created_at")
    logger.info(f"News list")
    return render(request, "news/news_list.html", {"news": news})


def news_view(request, slug):
    news = News.objects.get(slug=slug)
    return render(request, "news/news_view.html", {"news": news})
