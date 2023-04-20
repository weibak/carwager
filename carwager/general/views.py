import datetime
import logging

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse

from auction.models import Bid, Auction
from general.forms import RegisterForm, AuthForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from showbill.forms import AdvertFiltersForm
from showbill.models import Advert
from showbill.queries import filter_adverts

logger = logging.getLogger(__name__)

account_activation_token = PasswordResetTokenGenerator


# user registry in our up
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            logger.info(form.cleaned_data)
            user = User(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            user.set_password(form.cleaned_data["password"])
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            token_generator = PasswordResetTokenGenerator()
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request, "Activation link has been sent to your email, please forward link in email")
            return redirect("auth")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


# activate user's account, take token from register function
def activate(request, uidb64, token):
    User = get_user_model()
    token_cheker = PasswordResetTokenGenerator()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and token_cheker.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("auth")
    else:
        return HttpResponse('Activation link is invalid!')


# sign user in profile
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


# logout user from system
def logout_view(request):
    logout(request)
    return render(
        request,
        "logout.html",
    )


# profile view, show user's profile
def profile_view(request):
    if request.user.is_anonymous:
        return redirect("auth")
    user = request.user
    cars = Advert.objects.filter(owner=request.user).all()
    auctions = Bid.objects.filter(user=request.user).all()
    favorite_auctions = Auction.objects.filter(favorites__in=[user]).all()
    favorite_adverts = Advert.objects.filter(favorites__in=[user]).all()
    logger.info(f"Favorite auctions: {favorite_auctions} of {user}")
    logger.info(f"Favorite adverts: {favorite_adverts} of {user}")
    logger.info(f"Adverts of {request.user}: {cars}")
    logger.info(f"Bids of {request.user}: {auctions}")
    filters_form = AdvertFiltersForm(request.GET)
    auc_filter_form = AdvertFiltersForm(request.GET)
    time = datetime.datetime.now()

    return render(
        request,
        "profile.html", {
            "user": user,
            "adverts": cars,
            "auctions": auctions[0:4],
            "favorite_auctions": favorite_auctions,
            "favorite_adverts": favorite_adverts,
            "time": time,
        },
    )



"""    if filters_form.is_valid():
        order_date = filters_form.cleaned_data["order_date"]
        cars = filter_adverts(cars, order_date)

    if auc_filter_form.is_valid():
        order_date = auc_filter_form.cleaned_data["order_date"]
        auctions = filter_adverts(auctions, order_date)"""