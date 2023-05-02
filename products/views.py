from django.shortcuts import render,HttpResponseRedirect
from products.models import *
from users.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def index(request):
    context = {
        'title':'Store',
    }
    return render(request,'products/index.html',context)


#модифицированная ф-ция для фильтрации по категориям
def products(request,category_id=0,page=1):

    if category_id:
        category = ProductCategory.objects.get(id=category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    paginator = Paginator(products,3)
    products_paginator = paginator.page(page)

    context = {
        'title': 'Store - каталог',
        'categories': ProductCategory.objects.all(),
        'products':products_paginator,
        'selected_cat': category_id,
    }
    return render(request,'products/products.html',context)





# обработчик длядобавления товаров в корзину
@login_required
def basket_add(request,product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user,product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user,product=product,quantity=1)
    else:
        basket = baskets.first()
        basket.quantity+=1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def basket_remove(request,basket_id):
    basket= Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
