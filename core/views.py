from django.shortcuts import render
from .models import Recipe , GroceryItem,Favorite
from accounts.models import NutritionProfile
from django.contrib.auth.decorators import login_required

def home_view(request):
    recipes = Recipe.objects.filter(is_featured=True)[:4]
    return render(request, "home.html", {"recipes": recipes})

def recipes_view(request):
    recipes = Recipe.objects.all()
    q = request.GET.get("q", "")
    meal_type = request.GET.get("meal_type", "")
    nutrition = request.GET.get("nutrition", "")

    if q:
        recipes = recipes.filter(title__icontains=q)
    if meal_type:
        recipes = recipes.filter(meal_type=Recipe.MEAL_TYPES)
    if nutrition:
        recipes = recipes.filter(nutrition_category=Recipe.CATEGORIES)

    return render(request, "recipes.html", {"recipes": recipes,"q": q,"meal_type": meal_type,"nutrition": nutrition,"meal_types": Recipe.MEAL_TYPES,"nutrition_categories": Recipe.CATEGORIES,})

def about_view(request):
    return render(request, "about.html")

@login_required
def dashboard_view(request):
    profile = NutritionProfile.objects.filter(user=request.user).first()
    recipes = Recipe.objects.filter(is_featured=True)[:4]
    favorites_count = Favorite.objects.filter(user=request.user).count()
    grocery_count = GroceryItem.objects.filter(user=request.user,is_purchased=False).count()
    bmi = None
    if profile and profile.height > 0:
        height_in_meters = profile.height / 100
        bmi = round(profile.weight / (height_in_meters ** 2), 1)

    return render(request, "dashboard.html", {"profile": profile,"recipes": recipes,"favorites_count": favorites_count,"grocery_count": grocery_count,"bmi": bmi,})
