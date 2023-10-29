from main.models import Account
from book.models import Book
from django.contrib.auth.models import User
from daftar_belanja.models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
import json

@login_required(login_url='/login')
def shopping_cart(request):
    account = Account.objects.get(user=request.user)
    cart, created = ShoppingCart.objects.get_or_create(account=account)

    context = {
        'user': request.user.username,
        'account': account,
        'cart': cart.cart.all,
    }

    if not cart.cart.all():
        context['cart_empty'] = True
    else:
        context['cart_empty'] = False

    return render(request, 'shopping_cart.html', context)

@login_required(login_url='/login')
def owned_books(request):
    account = Account.objects.get(user=request.user)
    cart, created = ShoppingCart.objects.get_or_create(account=account)

    context = {
        'user': request.user.username,
        'account': account,
        'books': cart.owned_books.all,
    }

    if not cart.owned_books.all():
        context['no_books'] = True
    else:
        context['no_books'] = False

    return render(request, 'owned_books.html', context)

def get_shopping_cart(request):
    account = Account.objects.get(user=request.user)
    cart = ShoppingCart.objects.get(account=account)
    return HttpResponse(serializers.serialize('json', cart.cart.all()))

def get_owned_books(request):
    account = Account.objects.get(user=request.user)
    cart = ShoppingCart.objects.get(account=account)
    return HttpResponse(serializers.serialize('json', cart.owned_books.all()))

def add_to_cart(request, id):
    account = Account.objects.get(user=request.user)
    cart, created = ShoppingCart.objects.get_or_create(account=account)
    book = Book.objects.get(pk=id)
    books = Book.objects.all()

    context = {
        'books': books,
    }

    cart.cart.add(book)
    return render(request, 'katalog_buku.html', context)

@csrf_exempt
def add_to_cart_ajax(request):
    if request.method == 'POST':
        pk = json.loads(request.body).get('pk')
        account = Account.objects.get(user=request.user)
        cart, created = ShoppingCart.objects.get_or_create(account=account)
        book = Book.objects.get(pk=pk)
        cart.cart.add(book)

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def remove_from_cart_ajax(request):
    if request.method == 'DELETE':
        pk = json.loads(request.body).get('pk')
        account = Account.objects.get(user=request.user)
        cart, created = ShoppingCart.objects.get_or_create(account=account)
        book = Book.objects.get(pk=pk)
        cart.cart.remove(book)
        return HttpResponse(b"DELETED", 201)

    return HttpResponseNotFound()

@csrf_exempt
def delete_book_ajax(request):
    if request.method == 'DELETE':
        pk = json.loads(request.body).get('pk')
        account = Account.objects.get(user=request.user)
        cart, created = ShoppingCart.objects.get_or_create(account=account)
        book = Book.objects.get(pk=pk)
        cart.owned_books.remove(book)
        return HttpResponse(b"DELETED", 201)

    return HttpResponseNotFound()

@csrf_exempt
def confirm_payment(request):
    if request.method == 'POST':
        receiver = User.objects.get(username = request.POST.get("receiver"))
        # account = Account.objects.get(full_name = request.POST.get("receiver"))
        giver = Account.objects.get(user = request.user)
        account = Account.objects.get(user = receiver)
        receiver_cart, created = ShoppingCart.objects.get_or_create(account=account)
        giver_cart, created = ShoppingCart.objects.get_or_create(account=giver)
        for book in receiver_cart.cart.all():
            # if book not in receiver_cart.owned_books.all():
            receiver_cart.owned_books.add(book)

        giver_cart.cart.clear()
        
        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponseNotFound()

@csrf_exempt
def check_book_ownership(request):
    if request.method == 'GET':
        pk = request.GET.get('pk') 

        account = Account.objects.get(user=request.user)
        book = Book.objects.get(pk=pk)
        cart, created = ShoppingCart.objects.get_or_create(account=account)
        is_owned = cart.owned_books.filter(pk=book.pk).exists()

        data = {'is_owned': is_owned}
        return JsonResponse(data)