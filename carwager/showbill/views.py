from django.shortcuts import render, redirect
import logging
from showbill.forms import CarForm
from showbill.models import Car


logger = logging.getLogger(__name__)
