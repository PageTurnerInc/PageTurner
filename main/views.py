from main.models import Account
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from main.forms import CreateAccountForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
import datetime

from book.models import Book

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("katalog_buku:show_katalog"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Invalid username/password!')
            
    books = [Book.objects.get(id=1), Book.objects.get(id=2), Book.objects.get(id=100)]

    context = {
        'books': books,
    }

    return render(request, 'login.html', context)

@login_required(login_url='')
def logout_user(request):
    logout(request)
    response = redirect('main:login_user')
    response.delete_cookie('last_login')
    return response

def create_account(request):
    form = CreateAccountForm()

    if request.method == "POST":
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            Account.objects.create(
                user = new_user,
                full_name = new_user.full_name,
                email = new_user.email,
                is_premium = new_user.is_premium,
                )
            
            messages.success(request, 'Sign up successful!')
            return redirect('main:login_user')
    
    context = {'form': form}
    return render(request, 'create_account.html', context)