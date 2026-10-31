from django.shortcuts import render,redirect
from .models import CustomUser,EmailConfirmation
from .helpers import custom_send_email_confirmation,send_reset_password_email
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username:
            return render(request,"register.html",{"error":"Username is required"})
        
        if not email:
            return render(request,"register.html",{"error":"Email is required"})
        print(password1)
        print(password2)
        if  password1 != password2:
            return render(request,"register.html",{"error":"Password do not match"})

        if CustomUser.objects.filter(email=email).exists():
            return render(request,"register.html",{"error":"User with this email already exists"})
        
        if CustomUser.objects.filter(username=username).exists():
            return render(request,"register.html",{"error":"User with this username already exists"})
        user = CustomUser.objects.create_user(username=username,email=email,password=password2)
        token = EmailConfirmation.objects.create(user=user)
        custom_send_email_confirmation(token=token)
        return HttpResponse("check your email")

    return render(request,"register.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if not user:
            return render(request,"login.html",{"error":"Incorrect Credintials"})

        login(request,user)

        return HttpResponse("login works")
    
    return render(request,"login.html")

def confirm_token_view(request, token):
    token = EmailConfirmation.objects.get(token=token)
    token.user.is_active = True
    token.user.save()
    token.delete()

    return redirect("login")

def logout_view(request):
    logout(request)
    return redirect("login")


def change_password_view(request):
    if request.method == 'POST':
        old_password = request.POST.get("old_password")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if not request.user.check_password(old_password):
            return render(request, "change_password.html", {"error": "incorrect old password"})
        if password1 != password2:
            return render(request, "change_password.html", {"error": "Passwords do not match"})
        request.user.set_password(password1)
        request.user.save()
        return redirect("login")
    return render(request, "change_password.html")


def resend_email_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        user = CustomUser.objects.filter(email__iexact=email).first()
        if not user:
            return render(request, "resend.html", {"error": "User does not exist"})
        if user.is_active:
            return render(request, "resend.html", {"error": "Your email is already confirmed"})
        token = EmailConfirmation.objects.filter(user=user).first()
        if not token:
            token = EmailConfirmation.objects.create(user=user)
        custom_send_email_confirmation(token)
        return render(request, "resend.html", {"success": "Confirmation email sent. Check your inbox."})

    return render(request, "resend.html")


def resend_reset_email_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        user = CustomUser.objects.filter(email__iexact=email).first()

        if not user:
            return render(request, "reset_password.html", {"error": "User does not exist","email": email})

        token = EmailConfirmation.objects.filter(user=user).first()

        if not token:
            token = EmailConfirmation.objects.create(user=user)

        send_reset_password_email(token)

        return render(request, "reset_password.html", {"success": "Reset email sent. Check your inbox.","email": email})

    return redirect("reset_password")


def reset_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return HttpResponse("User does not exist")
        token = EmailConfirmation.objects.filter(user=user).first()
        if not token:
            token = EmailConfirmation.objects.create(user=user)
        send_reset_password_email(token)
        return HttpResponse("Check your email for the token")
    return render(request, "reset_password.html")


def confirm_reset_password_view(request, token):
    confirmation = EmailConfirmation.objects.filter(token=token).first()
    if not confirmation:
        return HttpResponse("Invalid or expired token")
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            return render(request, "confirm_reset_password.html", {"error": "Passwords do not match"})
        user = confirmation.user
        user.set_password(password1)
        user.save()
        confirmation.delete()
        return redirect("login")

    return render(request, "confirm_reset_password.html")

