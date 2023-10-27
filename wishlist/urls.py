from django.urls import path
from wishlist.views import add_to_wishlist,  show_wishlist, show_main,  delete_book, get_wishlist_items

app_name = 'wishlist'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('wishlist/', show_wishlist, name='show_wishlist'),
    path('add_to_wishlist/<int:book_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('delete_book/<int:book_id>/', delete_book, name='delete_book'),
    path('get_wishlist_items/', get_wishlist_items, name='get_wishlist_items'),
    
]