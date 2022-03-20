import logging

from django.http import HttpResponse

from auction.models import Auction, Bid
from general.forms import RegisterForm, AuthForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from showbill.forms import CarFiltersForm, AdvertFiltersForm
from showbill.models import Advert
from showbill.queries import filter_cars, filter_adverts

logger = logging.getLogger(__name__)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            logger.info(form.cleaned_data)
            user = User(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def sign_in(request):
    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.is_valid():
            logger.info(form.cleaned_data)
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/")
                else:
                    return HttpResponse("Disabled account")
            else:
                return redirect("register")
    else:
        form = AuthForm
    return render(request, "sign_in.html", {"form": form})


def logout_view(request):
    logout(request)
    return render(
        request,
        "logout.html",
    )


def profile_view(request):
    if request.user.is_anonymous:
        return redirect("auth")
    user = request.user
    cars = Advert.objects.filter(owner=request.user).all()
    auctions = Bid.objects.filter(user=request.user).all()
    logger.info(f"Adverts of {request.user}")
    filters_form = AdvertFiltersForm(request.GET)

    if filters_form.is_valid():
        order_by = filters_form.cleaned_data["order_by"]
        cars = filter_adverts(cars, order_by)

    return render(
        request,
        "profile.html", {
            "user": user,
            "adverts": cars,
            "auctions": auctions,
            "filters_form": filters_form}
    )
