"""
URL configuration for page_turner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path("api/books/", include("book.urls")),
<<<<<<< HEAD
    path("review/", include("review.urls")),
    path('daftar_belanja/', include('daftar_belanja.urls')),
    path('katalog/', include("katalog_buku.urls")),
]
=======
    path("rak_buku/", include("rak_buku.urls")),
    path('katalog/', include("katalog_buku.urls")),
    path('daftar_belanja/', include('daftar_belanja.urls')),
    ]
>>>>>>> 8c2200df75592afffdce8082ac89c27c0d65f2f4
