from django.contrib import admin
from .models import *

# Register your models here.
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('pname','pdesc',)
    search_fields = ('pname','pdesc',)
admin.site.register(Products,ProductsAdmin)