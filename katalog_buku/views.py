from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers
from django.http import HttpResponseRedirect
from book.models import Book
from rak_buku.models import Rak
from main.models import Account
from django.urls import reverse

def show_katalog(request):
    books = Book.objects.all()
    account = Account.objects.get(user=request.user)

    context = {
        'books': books,
        'account': account,
    }
    
    return render(request, "katalog_buku.html", context)

def show_book_page(request, id):
    book = Book.objects.get(pk=id)
    user = Account.objects.get(user=request.user)
    user_rak = Rak.objects.filter(user=user)
    
    delete = False
    if user == book.user:
        delete = True

    context = {
        'book': book,
        'delete': delete,
        'user_rak': user_rak,
    }

    return render(request, "book_page.html", context)

@csrf_exempt
def add_book_katalog(request):
    if request.method == "POST":
        isbn = request.POST.get("isbn")
        book_title = request.POST.get("title")
        book_author = request.POST.get("author")
        year_of_publication = request.POST.get("year")
        publisher = request.POST.get("publisher")
        image = request.POST.get("image-url")
        user = Account.objects.get(user=request.user)

        new_book = Book(isbn=isbn, book_title=book_title, book_author=book_author, year_of_publication=year_of_publication, publisher=publisher, image_url_s=image, image_url_m=image, image_url_l=image, user=user)
        new_book.save()

        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponseNotFound()

def delete_book_katalog(request, id):
    book = Book.objects.get(pk=id)
    user = Account.objects.get(user=request.user)
    if user == book.user:
        book.delete()
    
    return redirect('katalog_buku:show_katalog')

def get_product_json(request):
    books = Book.objects.all()
    return HttpResponse(serializers.serialize('json', books))

# SALSA
def add_book_to_rak(request, id, rak_id):
    book = Book.objects.get(pk=id)
    rak = Rak.objects.get(pk=rak_id)
    rak.books.add(book)

    return HttpResponseRedirect(reverse('katalog_buku:show_book', args=[id]))