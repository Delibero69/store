from django.contrib import admin
from products.models import *

# Register your models here.
# admin.site.register(Product)

admin.site.register(ProductCategory)

from django.utils.html import format_html




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','quantity','category')
    fields = ('name','description',('price','quantity'),'category','image')
    search_fields = ('name',)
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product','quantity')
    extra = 1