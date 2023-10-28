from django.urls import path
from review.views import *

app_name = 'review'

urlpatterns = [
    path('<int:book_id>/', show_reviews_by_book_id, name='show_reviews_by_book_id'),
    path('json/', get_reviews_json, name='get_reviews_json'),
    path('create-review-ajax/<int:book_id>/', create_review_ajax, name="create_review_ajax"),
    path('delete-review-ajax/<int:review_id>/', delete_review_ajax, name="delete_review_ajax"),
    path('update-review-ajax/<int:review_id>/', update_review_ajax, name="update_review_ajax"),
    path('get-reviews-json-by-book-id/<int:book_id>/', get_reviews_json_by_book_id, name='get_reviews_json_by_book_id'),
    path('get-reviews-json-by-request-id/<int:book_id>/', get_reviews_json_by_request_id, name="get_reviews_json_by_request_id"),
    path('get-others-reviews-json/<int:book_id>/', get_others_reviews_json, name="get_others_reviews_json"),
    path('get-book-rating-by-book-id/<int:book_id>/', get_book_rating_by_book_id, name="get_book_rating_by_book_id")
]