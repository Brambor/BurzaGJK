from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.urls import reverse

from .forms import MakeOfferForm, LoginForm
from .models import Offer, User


def general_list(request, **kwargs):
	offers = Offer.objects.all()
	if request.user.is_authenticated:
		user = request.user.id
	else:
		user = -1

	context = {
		'user': user,
	}
	
	q = request.GET.get('book_id', False)
	if q:
		offers = offers.filter(book=q)

		template = loader.get_template('grid_of_offers_for_one_book.html')
	else:
		template = loader.get_template('grid_of_offers.html')

	form = False
	q = request.GET.get('type', False)
	if q:
		if q == 'buy':
			offers = offers.exclude(vendor=user)
		elif request.user.is_authenticated:
			if q == 'sell':
				offers = offers.filter(active=True, vendor=user)
				form = MakeOfferForm()
			else:
				form = False

			if q == 'history':
				offers = offers.filter(active=False, vendor=user)

			if q == 'bit':
				#superusers are logged in but are not in User so this throws and error
				offers = offers.filter(buyer__in=[User.objects.get(id=user)])
		else:
			return redirect('clusters_all')

	context['offers'] = offers
	context['form'] = form
	return HttpResponse(template.render(context, request))

def cluster_list(request):
	if request.user.is_authenticated:
		user = request.user.id
	else:
		user = -1
	offers = Offer.objects.all().filter(active=True).exclude(vendor=user)
	clusters = {}
	for offer in offers:
		if offer.book.name in clusters:
			clusters[offer.book.name]['min_price'] = min(
				clusters[offer.book.name]['min_price'],
				offer.price,
			)
			clusters[offer.book.name]['max_price'] = max(
				clusters[offer.book.name]['max_price'],
				offer.price,
			)
			clusters[offer.book.name]['amount'] += 1
		else:
			clusters[offer.book.name] = {
				'image': offer.book.image.url,
				'book_author': offer.book.author,
				'book_name': offer.book.name,
				'min_price': offer.price,
				'max_price': offer.price,
				'amount': 1,
				'book_id': offer.book.id,
			}

	cluster_offers = []
	for c in clusters:
		if clusters[c]['amount'] == 1:
			clusters[c]['price'] = clusters[c]['min_price']
		else:
			clusters[c]['price'] = '{min_price} - {max_price}'.format(
				min_price=clusters[c]['min_price'],
				max_price=clusters[c]['max_price'],
			)
		del clusters[c]['min_price']
		del clusters[c]['max_price']

		cluster_offers.append(clusters[c])

	context = {
		'clusters': cluster_offers,
		'user': user,
	}

	template = loader.get_template('grid_of_clusters.html')
	return HttpResponse(template.render(context, request))

def offer_detail(request, offer):
	if request.user.is_authenticated:
		user = request.user.id
	else:
		user = -1
	context = {
		'offer': get_object_or_404(Offer, id=offer),
		'user': user,
	}

	template = loader.get_template('offer_detail.html')
	return HttpResponse(template.render(context, request))

#create user
#user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

def login_view(request):
	
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		print(username, password)
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
		else:
			return redirect('login')

		print(request.user, request.user.id)
		return redirect('clusters_all')
	else:
		context = {}
		context['form'] = LoginForm()
		template = loader.get_template('login.html')
		return HttpResponse(template.render(context, request))

def logout_view(request):
	logout(request)
	return redirect('clusters_all')

def process_sell(request):
	if request.user.is_authenticated:
		user = request.user.id
	else:
		return redirect('clusters_all')

	form = MakeOfferForm(request.POST)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.active = True
		instance.vendor = User.objects.get(id=user)

		instance.save()

	return HttpResponseRedirect('{}?type=sell'.format(reverse('general_filter')))

def process_buy(request):
	if request.user.is_authenticated:
		user = request.user.id
	else:
		return redirect('clusters_all')
	
	offer_id = request.POST['offer_id']

	o = Offer.objects.get(id=offer_id)

	o.buyer.add(User.objects.get(id=user))

	return HttpResponseRedirect(reverse('offer_detail', args=(offer_id)))
