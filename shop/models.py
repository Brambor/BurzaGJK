
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from itertools import chain

classes = chain(
	(('R{i}.A'.format(i=i), 'R{i}.A'.format(i=i)) for i in range(1, 9)),
	(('{n}.{clas}'.format(n=i, clas=clas), '{n}.{clas}'.format(n=i, clas=clas))
		for i in range(1, 5) for clas in ('A', 'B', 'C')),
)


class User(User):
	def __str__(self):
		return self.username

	class Meta:
		verbose_name = _('Uživatel')
		verbose_name_plural = _('Uživatelé')

	visited_class = models.CharField(
		max_length=255,
		choices=classes
	)


class Book(models.Model):
	def __str__(self):
		return '{author}: {name}'.format(
			author=self.author,
			name=self.name,
		)

	class Meta:
		verbose_name = _('Kniha')
		verbose_name_plural = _('Knihy')

	ISBN = models.CharField(
		max_length=255,  # 13char into four parts
	)
	author = models.CharField(
		max_length=255,
	)
	name = models.CharField(
		max_length=255,
	)
	image = models.ImageField()
	subject = models.CharField(
		max_length=255,
	)
	# google_books


class AbstractOffer(models.Model):
	class Meta:
		verbose_name = _('Abstraktní nabídka')
		verbose_name_plural = _('Abstraktní nabídky')

	price = models.IntegerField()
	negotiable = models.BooleanField()
	active = models.BooleanField()


class Offer(AbstractOffer):
	def __str__(self):
		return 'vendor: {vendor}, book: {book}, price: {price} Kč'.format(
			vendor=self.vendor.username,
			book=self.book.name,
			price=self.price,
		)

	class Meta:
		verbose_name = _('Nabídka')
		verbose_name_plural = _('Nabídky')

	vendor = models.ForeignKey(
		User,
		related_name='offer',
	)
	buyer = models.ManyToManyField(
		User,
		related_name='purchase',
		blank=True,
	)
	book = models.ForeignKey(
		Book,
	)
	description = models.CharField(
		max_length=255,
		blank=True,
	)
	will_be_active = models.DateField(
		blank=True,
		null=True,
	)
