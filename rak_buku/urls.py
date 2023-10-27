from django.urls import path
from rak_buku.views import *


app_name = 'rak_buku'

urlpatterns = [
    path('', show_rak, name='show_rak'),
    path('json/', show_json, name='show_json'), 
    path('<int:id>/', show_rak_by_id, name='show_rak_by_id'), 
    path('create-rak', create_rak, name='create_rak'),
    path('get-rak/', get_rak_json, name='get_rak_json'),
    path('create-ajax/', add_rak_ajax, name='add_rak_ajax')
]