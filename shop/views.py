from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from .models import Offer, User


def offer_list(request, **kwargs):
	try:
		user = request.session["logged_in"]
	except KeyError:
		user = False
	offers = Offer.objects.all().filter(active=True).exclude(vendor=user)
	try:
		book_id = kwargs["book_id"]
		offers = offers.filter(book=book_id)
	except KeyError:
		print("fcked up")
	context = {
		"offers": offers,
		"user": user,
	}

	template = loader.get_template('grid_of_offers.html')
	return HttpResponse(template.render(context, request))

def cluster_list(request):
	try:
		user = request.session["logged_in"]
	except KeyError:
		user = False
	offers = Offer.objects.all().filter(active=True).exclude(vendor=user)
	clusters = {}
	for offer in offers:
		if offer.book.name in clusters:
			clusters[offer.book.name]["min_price"] = min(
				clusters[offer.book.name]["min_price"],
				offer.price,
			)
			clusters[offer.book.name]["max_price"] = max(
				clusters[offer.book.name]["max_price"],
				offer.price,
			)
			clusters[offer.book.name]["amount"] += 1
		else:
			clusters[offer.book.name] = {
				# image
				"book_author": offer.book.author,
				"book_name": offer.book.name,
				"min_price": offer.price,
				"max_price": offer.price,
				"amount": 1,
				"book_id": offer.book.id,
			}

	cluster_offers = []
	for c in clusters:
		cluster_offers.append(clusters[c])

	context = {
		"clusters": cluster_offers,
		"user": user,
	}

	template = loader.get_template('grid_of_clusters.html')
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
