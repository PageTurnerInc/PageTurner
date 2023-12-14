from django.urls import path
from katalog_buku.views import show_katalog, show_book_page, add_book_katalog, get_product_json, delete_book_katalog, add_book_to_rak, show_json, add_book_katalog_flutter

app_name = 'katalog_buku'

urlpatterns = [
    path('', show_katalog, name='show_katalog'),
    path('book/<int:id>/', show_book_page, name='show_book'),
    path('add-book-katalog/', add_book_katalog, name='add_book_katalog'),
    path('delete-book-katalog/<int:id>', delete_book_katalog, name='delete_book_katalog'),
    path('get-product/', get_product_json, name='get_product_json'),
    path('book/<int:id>/<int:rak_id>/', add_book_to_rak, name='add_book_to_rak'),
    path('json/', show_json, name='show_json'),
    path('add-book-katalog-flutter/', add_book_katalog_flutter, name='add-book-katalog-flutter'),
]