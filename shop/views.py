from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.urls import reverse

from django.db.models import Count

from .forms import AddBookForm, MakeOfferForm, LoginForm
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
				#superusers are logged in but are not in User so this throws an error
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

def offer_list_for_one_book(request, book_id):
	if request.user.is_authenticated:
		user = request.user.id
	else:
		user = -1

	context = {'user': user}

	offers = Offer.objects.all()
	offers = offers.filter(book=book_id)
	offers = offers.exclude(vendor=user)
	context['offers'] = offers

	template = loader.get_template('grid_of_offers_for_one_book.html')
	return HttpResponse(template.render(context, request))

def offer_detail(request, offer_id):
	if request.user.is_authenticated:
		user = request.user.id
	else:
		user = -1

	offer = get_object_or_404(Offer, id=offer_id)

	if request.method == 'POST':
		if (user == -1) or (request.user.id != offer.vendor.id):
			return redirect('clusters_all')

		offer.delete()
		response = redirect('general_filter')
		response['Location'] += '?type=sell'  #success message
		return response
	else:
		context = {
			'offer': offer,
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
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
		else:
			return redirect('login')

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

	response = reverse('offer_detail', kwargs={'offer_id': offer_id}) # success message

	return HttpResponseRedirect(response)

def add_book(request):
	if request.user.is_authenticated:
		context = {'user': request.user.id}
	else:
		return redirect('clusters_all')

	template = loader.get_template('add_book.html')

	if request.method == 'POST':
		form = AddBookForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			response = redirect('general_filter')
			response['Location'] += '?type=sell'  #success message
			return response
	else:
		context['form'] =  AddBookForm()

	return HttpResponse(template.render(context, request))

def transact_list(request):
	if request.user.is_authenticated:
		user = request.user.id
		context = {'user': user}
	else:
		return redirect('clusters_all')

	offers = Offer.objects.all()
	offers = offers.filter(vendor=user)
	offers = offers.annotate(num_buyers=Count('buyer'))
	offers = offers.filter(num_buyers__gte=1)
	context['offers'] = offers

	template = loader.get_template('transact_list.html')
	return HttpResponse(template.render(context, request))

def transact_detail(request, offer_id):
	if request.user.is_authenticated:
		user = request.user.id
		context = {'user': user}
	else:
		return redirect('clusters_all')

	offer = get_object_or_404(Offer, id=offer_id)
	buyers = User.objects.filter(purchase=offer)

	context = {
		'offer': offer,
		'buyers': buyers,
		'user': user,
	}
	template = loader.get_template('transact_detail.html')
	return HttpResponse(template.render(context, request))
