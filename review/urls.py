from django.urls import path
from review.views import *

app_name = 'review'

urlpatterns = [
    path('<int:book_id>/', show_reviews_by_book_id, name='show_reviews_by_book_id'),
    path('json/', get_reviews_json, name='get_reviews_json'),
    path('create-review-ajax/<int:book_id>/', create_review_ajax, name="create_review_ajax"),
    path('create-review-flutter/<int:book_id>/', create_review_flutter, name="create_review_flutter"),
    path('delete-review-ajax/<int:review_id>/', delete_review_ajax, name="delete_review_ajax"),
    path('delete-review-flutter/', delete_review_flutter, name="delete_review_flutter"),
    path('update-review-ajax/<int:review_id>/', update_review_ajax, name="update_review_ajax"),
    path('update-review-flutter/<int:review_id>/', update_review_flutter, name="update_review_flutter"),
    path('get-reviews-json-by-book-id/<int:book_id>/', get_reviews_json_by_book_id, name='get_reviews_json_by_book_id'),
    path('get-reviews-json-by-request-id/<int:book_id>/', get_reviews_json_by_request_id, name="get_reviews_json_by_request_id"),
    path('get-others-reviews-json/<int:book_id>/', get_others_reviews_json, name="get_others_reviews_json"),
    path('get-book-rating-by-book-id/<int:book_id>/', get_book_rating_by_book_id, name="get_book_rating_by_book_id"),
    path('add-review/<int:book_id>/', add_review, name="add_review"),
    path('get-book-ratings/', get_book_ratings, name="get_book_ratings"),
    path('get-rating-percentage/<int:book_id>/<int:target_rating>/', get_rating_percentage, name="get_rating_percentage")
]