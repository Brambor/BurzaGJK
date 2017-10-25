from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from .models import Offer, User


def offer_list(request):
	try:
		user = request.session["logged_in"]
	except KeyError:
		user = False
	context = {
		"offers": Offer.objects.all().filter(active=True).exclude(vendor=user),
		"user": user,
	}

	template = loader.get_template('grid_of_offers.html')
	return HttpResponse(template.render(context, request))

def offer_detail(request, offer):
	try:
		user = request.session["logged_in"]
	except KeyError:
		user = False
	context = {
		"offer": get_object_or_404(Offer, id=offer),
		"user": user,
	}

	template = loader.get_template('offer_detail.html')
	return HttpResponse(template.render(context, request))

def sell_list(request):
	try:
		user = request.session["logged_in"]
	except KeyError:
		user = False
	context = {
		"offers": Offer.objects.all().filter(active=True, vendor=user),
		"user": user,
	}

	template = loader.get_template('grid_of_offers.html')
	return HttpResponse(template.render(context, request))

def history_list(request):
	try:
		user = request.session["logged_in"]
	except KeyError:
		user = False
	context = {
		"offers": Offer.objects.all().filter(active=False, vendor=user),
		"user": user,
	}

	template = loader.get_template('grid_of_offers.html')
	return HttpResponse(template.render(context, request))

def login(request):
	request.session["logged_in"] = User.objects.all()[0].id
	return redirect("offers_all")

def logout(request):
	del request.session["logged_in"]
	return redirect("offers_all")
