from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import loader

from .forms import MakeOfferForm
from .models import Offer, User


def general_list(request, **kwargs):
	offers = Offer.objects.all()
	try:
		user = int(request.session["logged_in"])
	except KeyError:
		user = -1

	context = {
		"user": user,
	}
	try:
		q = request.GET["book_id"]
		offers = offers.filter(book=q)

		template = loader.get_template('grid_of_offers_for_one_book.html')
	except KeyError:
		template = loader.get_template('grid_of_offers.html')

	try:
		q = request.GET["type"]
		if q == "buy":
			offers = offers.exclude(vendor=user)
		if q == "sell":
			offers = offers.filter(active=True, vendor=user)
			
			form = MakeOfferForm()
		else:
			form = False
		if q == "history":
			offers = offers.filter(active=False, vendor=user)
	except KeyError:
		form = False

	context["offers"] = offers
	context["form"] = form
	return HttpResponse(template.render(context, request))

def cluster_list(request):
	try:
		user = int(request.session["logged_in"])
	except KeyError:
		user = -1
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
				"image": offer.book.image.url,
				"book_author": offer.book.author,
				"book_name": offer.book.name,
				"min_price": offer.price,
				"max_price": offer.price,
				"amount": 1,
				"book_id": offer.book.id,
			}

	cluster_offers = []
	for c in clusters:
		if clusters[c]["amount"] == 1:
			clusters[c]["price"] = clusters[c]["min_price"]
		else:
			clusters[c]["price"] = "{min_price} - {max_price}".format(
				min_price=clusters[c]["min_price"],
				max_price=clusters[c]["max_price"],
			)
		del clusters[c]["min_price"]
		del clusters[c]["max_price"]

		cluster_offers.append(clusters[c])

	context = {
		"clusters": cluster_offers,
		"user": user,
	}

	template = loader.get_template('grid_of_clusters.html')
	return HttpResponse(template.render(context, request))

def offer_detail(request, offer):
	try:
		user = int(request.session["logged_in"])
	except KeyError:
		user = -1
	context = {
		"offer": get_object_or_404(Offer, id=offer),
		"user": user,
	}

	template = loader.get_template('offer_detail.html')
	return HttpResponse(template.render(context, request))


def login(request):
	request.session["logged_in"] = User.objects.all()[0].id
	return redirect("clusters_all")

def logout(request):
	del request.session["logged_in"]
	return redirect("clusters_all")
