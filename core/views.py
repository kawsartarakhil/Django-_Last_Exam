from django.db.models import Q
from django.shortcuts import render
from .models import Recipe , GroceryItem,Favorite,MealSuggestion
from accounts.models import NutritionProfile
from django.contrib.auth.decorators import login_required
from groq import Groq
from django.conf import settings

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
@login_required
def meal_suggestions_view(request):
    suggested_recipes = []
    ingredients_entered = ""
    generated_recipe = ""
    error = ""

    if request.method == "POST":
        ingredients_entered = request.POST.get("ingredients", "").strip()
        action = request.POST.get("action")

        if ingredients_entered:

            if action == "match":
                ingredients = [item.strip() for item in ingredients_entered.split(",") if item.strip()]
                query = Q()
                for ingredient in ingredients:
                    query |= Q(ingredients__icontains=ingredient)
                suggested_recipes = Recipe.objects.filter(query).distinct()[:10]

                for recipe in suggested_recipes:
                    MealSuggestion.objects.create(user=request.user,ingredients_entered=ingredients_entered,recipe=recipe)

                if not suggested_recipes:
                    error = "No matching recipes found."

            elif action == "generate":
                if not settings.GROQ_API_KEY:
                    error = "Groq API key is not configured."
                else:
                    try:
                        client = Groq(api_key=settings.GROQ_API_KEY)

                        response = client.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "You are a helpful recipe assistant. "
                                        "Create practical, balanced recipes. "
                                        "Include a title, description, "
                                        "number of servings, ingredients, "
                                        "and step-by-step instructions."
                                    )
                                },
                                {
                                    "role": "user",
                                    "content": (
                                        f"Create a recipe using these "
                                        f"ingredients: {ingredients_entered}"
                                    )
                                }
                            ]
                        )

                        generated_recipe = response.choices[0].message.content

                        MealSuggestion.objects.create(user=request.user,ingredients_entered=ingredients_entered,generated_recipe=generated_recipe)
                    except Exception as e:
                        print(e)
                        error = "Could not generate a recipe. Please try again."

        else:
            error = "Please enter some ingredients."

    previous_suggestions = MealSuggestion.objects.filter(user=request.user).select_related("recipe").order_by("-created_at")[:20]

    return render(request, "meal_suggestions.html", {"suggested_recipes": suggested_recipes,"ingredients_entered": ingredients_entered,"generated_recipe": generated_recipe, "previous_suggestions": previous_suggestions,"error": error,})