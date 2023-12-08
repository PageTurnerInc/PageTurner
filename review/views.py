import json
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime

from book.models import Book
from review.forms import ReviewForm
from review.models import *

# Create your views here.
@login_required(login_url='/login')
def add_review(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    form = ReviewForm(request.POST or None, initial={'book': book, 'user': request.user})

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.date = datetime.now()
            review.save()

            book_rating, created = BookRating.objects.get_or_create(book=book)
            print(book_rating)
            if not created:
                total_reviews = Review.objects.filter(book=book).count()
                total_ratings = float(sum([review.rating for review in Review.objects.filter(book=book)]))
                if total_reviews != 0:
                    book_rating.rating = total_ratings / total_reviews
                else:
                    book_rating.rating = float(review.rating)
            else:
                book_rating.rating = review.rating

            book_rating.save()

            return HttpResponseRedirect(reverse('review:show_reviews_by_book_id', args=(book_id,)))

    context = {'form': form, 'name': request.user.username}
    return render(request, "make_review.html", context)

@csrf_exempt
@login_required(login_url='/login')
def add_review_flutter(request, book_id):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        book = get_object_or_404(Book, pk=book_id)
        rating = int(data.get('rating'))
        comment = data.get('comment')
        reviewer = request.user.username
        date = datetime.now()

        if comment == "":
            comment = ""

        new_review = Review(user=user, book=book, reviewer=reviewer, 
                        rating=rating, comment=comment, date=date)
        
        try:
            new_review.full_clean()
        except ValidationError as e:
            return JsonResponse({"status": "error"}, status=422)

        new_review.save()

        book_rating, created = BookRating.objects.get_or_create(book=book)
        print(book_rating)
        if not created:
            total_reviews = Review.objects.filter(book=book).count()
            total_ratings = float(sum([review.rating for review in Review.objects.filter(book=book)]))
            if total_reviews != 0:
                book_rating.rating = total_ratings / total_reviews
            else:
                book_rating.rating = float(new_review.rating)
        else:
            book_rating.rating = new_review.rating

        book_rating.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

def get_book_rating_by_book_id(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    rating = BookRating.objects.filter(book=book)
    return HttpResponse(serializers.serialize("json", rating), content_type="application/json")

def get_book_ratings(request):
    ratings = BookRating.objects.all()
    return HttpResponse(serializers.serialize("json", ratings), content_type="application/json")

def get_reviews_json(request):
    reviews = Review.objects.all()
    return HttpResponse(serializers.serialize("json", reviews), content_type="application/json")

def get_others_reviews_json(request, book_id):
    user = request.user
    book = get_object_or_404(Book, pk=book_id)
    reviews = Review.objects.filter(book=book).exclude(user=user)
    return HttpResponse(serializers.serialize("json", reviews), content_type="application/json")

def get_reviews_json_by_book_id(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = Review.objects.filter(book=book).order_by('-date')
    return HttpResponse(serializers.serialize("json", reviews), content_type="application/json")

def get_reviews_json_by_request_id(request, book_id):
    user = request.user
    book = get_object_or_404(Book, pk=book_id)
    reviews = Review.objects.filter(user=user, book=book)
    return HttpResponse(serializers.serialize("json", reviews), content_type="application/json")

@login_required(login_url='/login')
def show_reviews_by_book_id(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = Review.objects.filter(book=book).order_by('-date')
    book_rating = BookRating.objects.filter(book=book)
    # print(book_rating.fields.rating)
    context = {
        'book': book,
        'reviews': reviews,
        'book_rating': book_rating,
    }

    return render(request, 'show_reviews_by_book_id.html', context)

def get_rating_percentage(request, book_id, target_rating):
    try:
        target_rating = int(target_rating)
        if target_rating < 1 or target_rating > 5:
            raise ValueError('Invalid target rating value')

        book = get_object_or_404(Book, pk=book_id)
        review_count = Review.objects.filter(book=book).count()
        target_review_count = Review.objects.filter(book=book, rating=target_rating).count()

        target_percentage = (target_review_count / review_count) * 100 if review_count > 0 else 0
        # print(target_percentage)

        return JsonResponse({'rating_{}_percentage'.format(target_rating): target_percentage, 'count_{}'.format(target_rating): target_review_count})
    
    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
@login_required(login_url='/login')
def create_review_ajax(request, book_id):
    if request.method == 'POST':
        # print(request.POST)
        # print(request.POST.get("rating"))
        user = request.user
        book = get_object_or_404(Book, pk=book_id)
        data = json.loads(request.body)
        rating = int(data.get('rating'))
        comment = data.get('comment')
        reviewer = request.user.username
        date = datetime.now()

        if comment == "":
            comment = ""

        new_review = Review(user=user, book=book, reviewer=reviewer, rating=rating, comment=comment, date=date)

        try:
            new_review.full_clean()
        except ValidationError as e:
            return HttpResponse(str(e), status=400)

        new_review.save()

        book_rating, created = BookRating.objects.get_or_create(book=book)
        print(book_rating)
        if not created:
            total_reviews = Review.objects.filter(book=book).count()
            total_ratings = float(sum([review.rating for review in Review.objects.filter(book=book)]))
            if total_reviews != 0:
                book_rating.rating = total_ratings / total_reviews
            else:
                book_rating.rating = float(new_review.rating)
        else:
            book_rating.rating = new_review.rating

        book_rating.save()

        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()

@csrf_exempt
@login_required(login_url='/auth/login')
def create_review_flutter(request, book_id):
    if request.method == 'POST':
        # print(request.POST)
        # print(request.POST.get("rating"))
        user = request.user
        book = get_object_or_404(Book, pk=book_id)
        data = json.loads(request.body)
        rating = int(data.get('rating'))
        comment = data.get('comment')
        reviewer = request.user.username
        date = datetime.now()

        if comment == "":
            comment = ""

        new_review = Review(user=user, book=book, reviewer=reviewer, rating=rating, comment=comment, date=date)

        try:
            new_review.full_clean()
        except ValidationError as e:
            return HttpResponse(str(e), status=400)

        new_review.save()

        book_rating, created = BookRating.objects.get_or_create(book=book)
        print(book_rating)
        if not created:
            total_reviews = Review.objects.filter(book=book).count()
            total_ratings = float(sum([review.rating for review in Review.objects.filter(book=book)]))
            if total_reviews != 0:
                book_rating.rating = total_ratings / total_reviews
            else:
                book_rating.rating = float(new_review.rating)
        else:
            book_rating.rating = new_review.rating

        book_rating.save()

        return JsonResponse({"status": "success"}, status=201)
    return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
@login_required(login_url='/login')
def delete_review_ajax(request, review_id):
    if request.method == 'DELETE':
        review = get_object_or_404(Review, pk=review_id)

        if request.user == review.user:
            book = review.book

            review.delete()

            book_rating = BookRating.objects.get(book=book)
            total_reviews = Review.objects.filter(book=book).count()
            if total_reviews > 0:
                total_ratings = sum([review.rating for review in Review.objects.filter(book=book)])
                book_rating.rating = total_ratings / total_reviews
                book_rating.save()
            else:
                book_rating.rating = 0
                book_rating.delete()

            return HttpResponse("OK", status=204)
        else:
            return HttpResponse("Unauthorized", status=401) 
    return HttpResponseNotFound()

@csrf_exempt
@login_required(login_url='/auth/login')
def post_delete_review_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        review_id = data["review-id"]
        book_id = data["book-id"]
        review = get_object_or_404(Review, pk=review_id)

        if request.user == review.user:
            book = get_object_or_404(Book, pk=book_id)

            review.delete()

            book_rating = BookRating.objects.get(book=book)
            total_reviews = Review.objects.filter(book=book).count()
            if total_reviews > 0:
                total_ratings = sum([review.rating for review in Review.objects.filter(book=book)])
                book_rating.rating = total_ratings / total_reviews
                book_rating.save()
            else:
                book_rating.rating = 0
                book_rating.delete()

            return JsonResponse({"status": "success"}, status=204)
    return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
@login_required(login_url='/auth/login')
def delete_review_flutter(request, review_id):
    if request.method == 'DELETE':
        review = get_object_or_404(Review, pk=review_id)

        if request.user == review.user:
            book = review.book

            review.delete()

            book_rating = BookRating.objects.get(book=book)
            total_reviews = Review.objects.filter(book=book).count()
            if total_reviews > 0:
                total_ratings = sum([review.rating for review in Review.objects.filter(book=book)])
                book_rating.rating = total_ratings / total_reviews
                book_rating.save()
            else:
                book_rating.rating = 0
                book_rating.delete()

            return JsonResponse({"status": "success"}, status=204)
        else:
            return JsonResponse({"status": "unauthorized"}, status=401) 
    return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
@login_required(login_url='/login')
def update_review_ajax(request, review_id):
    if request.method == 'PATCH':
        data = json.loads(request.body)
        print(data)
        new_rating = data.get('rating')
        new_comment = data.get('comment')

        review = get_object_or_404(Review, pk=review_id)
        book = review.book

        print(book)
        if request.user == review.user:
            if new_rating is not None:
                review.rating = int(new_rating)
                review.date = datetime.now()
                review.save()

                book_rating = BookRating.objects.get(book=book)
                total_reviews = Review.objects.filter(book=book).count()
                total_ratings = sum([review.rating for review in Review.objects.filter(book=book)])
                book_rating.rating = total_ratings / total_reviews

                if total_reviews != 0:
                    book_rating.rating = total_ratings / total_reviews
                else:
                    book_rating.rating = 0  # Set a default value if there are no reviews
                book_rating.save()

            if new_comment != '':
                review.comment = new_comment
                review.save()

            return HttpResponse("OK", status=200)
        else:
            return HttpResponse("Unauthorized", status=401)
    return HttpResponseNotFound()

@csrf_exempt
@login_required(login_url='/auth/login')
def update_review_flutter(request, review_id):
    if request.method == 'PATCH':
        data = json.loads(request.body)
        print(data)
        new_rating = data.get('rating')
        new_comment = data.get('comment')

        review = get_object_or_404(Review, pk=review_id)
        book = review.book

        print(book)
        if request.user == review.user:
            if new_rating is not None:
                review.rating = int(new_rating)
                review.date = datetime.now()
                review.save()

                book_rating = BookRating.objects.get(book=book)
                total_reviews = Review.objects.filter(book=book).count()
                total_ratings = sum([review.rating for review in Review.objects.filter(book=book)])
                book_rating.rating = total_ratings / total_reviews

                if total_reviews != 0:
                    book_rating.rating = total_ratings / total_reviews
                else:
                    book_rating.rating = 0  # Set a default value if there are no reviews
                book_rating.save()

            if new_comment != '':
                review.comment = new_comment
                review.save()

            return JsonResponse({"status": "success"}, status=200)
        else:
            return JsonResponse({"status": "unauthorized"}, status=401)
    return JsonResponse({"status": "unauthorized"}, status=401)