from django.shortcuts import render
from .models import Recipe

def home_view(request):
    recipes = Recipe.objects.filter(is_featured=True)[:4]
    return render(request, "home.html", {"recipes": recipes})