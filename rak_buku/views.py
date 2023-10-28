from django.shortcuts import render, redirect
from rak_buku.models import Rak, RakForm
from main.models import Account
from book.models import Book
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect


# Create your views here.
def show_rak(request):
    all_rak = Rak.objects.all()
    user = Account.objects.get(user=request.user)
    user_rak = Rak.objects.filter(user=user)

    context = {
        'all_rak': all_rak,
        'user_rak': user_rak,
        'user': user
    }

    return render(request, "menu_rak.html", context)

def show_rak_by_id(request, id):
    rak = Rak.objects.get(pk=id)
    books_in_rak = rak.books.all()

    context = {
        'name': rak.name,
        'description': rak.description,
        'user': rak.user.full_name,
        'books': books_in_rak,
        'rak':rak
    }

    return render(request, "rak_buku.html", context)

def get_rak_json(request):
    user = Account.objects.get(user=request.user)
    user_rak = Rak.objects.filter(user=user)  # Filter Rak objects by the associated Account
    return HttpResponse(serializers.serialize('json', user_rak))

def get_rak_json_by_id(request, id):
    rak = Rak.objects.filter(pk=id)  # Filter Rak objects by the associated Account
    return HttpResponse(serializers.serialize('json', rak))

@csrf_exempt
def add_rak_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        description = request.POST.get("description")
        user = Account.objects.get(user=request.user)

        new_rak = Rak(name=name, description=description, user=user)
        new_rak.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def edit_rak(request, id):
    rak = Rak.objects.get(pk=id)

    if request.method == 'POST':
        name = request.POST.get("name")
        description = request.POST.get("description")
        user = Account.objects.get(user=request.user)

        rak.name = name
        rak.description = description
        rak.save()

        return HttpResponseRedirect(reverse('rak_buku:show_rak_by_id', args=[id]))
    return HttpResponseNotFound()

def delete_book(request, rak_id, book_id):
        rak = Rak.objects.get(pk=rak_id)
        book = Book.objects.get(pk=book_id)

        rak.books.remove(book)

        return HttpResponseRedirect(reverse('rak_buku:show_rak_by_id', kwargs={'id': rak_id,}))

def delete_rak(request, id):
        rak = Rak.objects.get(pk=id)

        rak.delete()

        return HttpResponseRedirect(reverse('rak_buku:show_rak'))
