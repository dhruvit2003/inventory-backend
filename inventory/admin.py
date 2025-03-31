# Register your models here.
from django.contrib import admin
from .models import Item, BuyingTransaction, SellingTransaction

admin.site.register(Item)
admin.site.register(BuyingTransaction)
admin.site.register(SellingTransaction)