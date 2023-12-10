import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from main.models import Account

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            account = Account.objects.get(user=user)
            # Status login sukses.
            return JsonResponse({
                "user": user.pk,
                "username": user.username,
                "fullname": account.full_name,
                "email": account.email,
                "isPremium": account.is_premium,
                "status": True,
                "message": "Login successful!",
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed!"
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login failed!"
        }, status=401)

@csrf_exempt   
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)
    
@csrf_exempt
def register_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        is_premium = "Y" if data['is_premium'] == "Yes" else "N"

        user = User(
            username = data["username"],
            email = data["email"],
            password = data["password"],
        )
        user.save()

        account = Account(
            user = user,
            full_name = data["full_name"],
            email = data["email"],
            is_premium = is_premium,
        )
        account.save()

        return JsonResponse({"status": True,}, status=200)
    
    return JsonResponse({"status": False}, status=500)