from django.contrib import admin

from .models import Book, Offer, User


class BookAdmin(admin.ModelAdmin):
	pass


class ItemAdmin(admin.ModelAdmin):
	pass


class OfferAdmin(admin.ModelAdmin):
	pass


class UserAdmin(admin.ModelAdmin):
	pass


admin.site.register(Book, BookAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(User, UserAdmin)
