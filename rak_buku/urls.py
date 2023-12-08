from django.urls import path
from rak_buku.views import *


app_name = 'rak_buku'

urlpatterns = [
    path('', show_rak, name='show_rak'),
    path('<int:id>/', show_rak_by_id, name='show_rak_by_id'), 
    path('get-rak/', get_rak_json, name='get_rak_json'),
    path('get-rak/<int:id>/', get_rak_json_by_id, name='get_rak_json_by_id'),
    path('edit-rak/<int:id>/', edit_rak, name='edit_rak'),
    path('delete-rak/<int:id>/', delete_rak, name='delete_rak'),
    path('create-ajax/', add_rak_ajax, name='add_rak_ajax'),

    path('get-rak/<int:id>/list-book/', get_book_json_by_id, name='get_book_json_by_id'),
    path('delete-book/<int:rak_id>/<int:book_id>/', delete_book, name='delete_book'),

    path('get-rak-all/', get_rak_json_all, name='get_rak_json_all'),

    path('create-rak-flutter/', add_rak_flutter, name='add_rak_flutter'),
    path('remove_book_from_rak_flutter/', remove_book_from_rak_flutter, name='remove_book_from_rak_flutter'),
    path('remove_rak_flutter/', remove_rak_flutter, name='remove_rak_flutter'),
]