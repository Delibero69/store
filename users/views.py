from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponseRedirect
from users.models import *
from users.forms import *
from django.contrib import auth, messages
from django.urls import reverse
from products.models import *
from django.contrib.auth.decorators import login_required
from cloudipsp import Api, Checkout

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("index"))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse("users:login"))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("users:profile"))
#     else:
#         form = UserProfileForm(instance=request.user)
#     context = {'title': 'Ваш профиль',
#                'form': form,
#                'baskets': Basket.objects.filter(user=request.user),
#                }
#     return render(request, 'users/profile.html', context)
#
#
#
#
#
# def add_to_cart(request):
#     api = Api(merchant_id=1397120,
#               secret_key='Not for tests. Test credentials: https://docs.fondy.eu/docs/page/2/ ')
#     checkout = Checkout(api=api)
#     data = {
#         "currency": "UAH",
#         "amount": BasketQuerySet.total_sum(),
#     }
#     url = checkout.url(data).get('checkout_url')
#     context = {
#         'title':'Store',
#         'url': url
#     }
#     return render(request, 'users/profile.html', context)


@login_required
def profile(request):
    api = Api(merchant_id=1397120,
              secret_key='Not for tests. Test credentials: https://docs.fondy.eu/docs/page/2/ ')
    checkout = Checkout(api=api)

    price = int(sum(basket.sum() for basket in Basket.objects.filter(user=request.user)))*100

    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("users:profile"))
    else:
        form = UserProfileForm(instance=request.user)
    if price:
        data = {
            "currency": "UAH",
            "amount": price,
        }
        url = checkout.url(data).get('checkout_url')
        context = {'title': 'Ваш профиль',
               'form': form,
               'baskets': Basket.objects.filter(user=request.user),
               'add_to_cart_url': url,
               }
    else:
        context = {'title': 'Ваш профиль',
                   'form': form,
                   'baskets': Basket.objects.filter(user=request.user),
                   }
    return render(request, 'users/profile.html', context)









def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))




