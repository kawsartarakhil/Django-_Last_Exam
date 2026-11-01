from django.db.models import Q
from django.shortcuts import render , redirect
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


def grocery_list_view(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add":
            name = request.POST.get("name", "").strip()
            quantity = request.POST.get("quantity", "").strip()

            if name:
                GroceryItem.objects.create(user=request.user, name=name,quantity=quantity)

        elif action == "toggle":
            item_id = request.POST.get("item_id")
            item = GroceryItem.objects.filter(id=item_id,user=request.user).first()

            if item:
                item.is_purchased = not item.is_purchased
                item.save()

        elif action == "delete":
            item_id = request.POST.get("item_id")
            item = GroceryItem.objects.filter(id=item_id,user=request.user).first()

            if item:
                item.delete()

    items = GroceryItem.objects.filter(user=request.user)
    return render(request, "grocery_list.html", {"items": items})


@login_required
def favorite_toggle_view(request, recipe_id):
    recipe = Recipe.objects.filter(id=recipe_id).first()

    if recipe:
        favorite = Favorite.objects.filter( user=request.user, recipe=recipe).first()
        if favorite:
            favorite.delete()
        else:
            Favorite.objects.create(user=request.user,recipe=recipe)

    if request.POST.get("next") == "favorites":
        return redirect("favorites")

    return redirect("recipes")



def favorites_view(request):
    favorites = Favorite.objects.filter( user=request.user).select_related("recipe")
    return render(request, "favorites.html", {"favorites": favorites})


def profile_view(request):
    profile = NutritionProfile.objects.filter(user=request.user).first()
    error = ""
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "update":
            username = request.POST.get("username", "").strip()
            email = request.POST.get("email", "").strip()
            bio = request.POST.get("bio", "").strip()
            try:
                age = int(request.POST.get("age"))
                height = float(request.POST.get("height"))
                weight = float(request.POST.get("weight"))
                gender = request.POST.get("gender")
                goal = request.POST.get("goal")
                food_preferences = request.POST.get("food_preferences", "").strip()
                allergies = request.POST.get("allergies", "").strip()

                if not username or not email:
                    raise ValueError

                if age <= 0 or height <= 0 or weight <= 0:
                    raise ValueError

                if gender not in ["male", "female"]:
                    raise ValueError

                if goal not in ["lose", "maintain", "gain"]:
                    raise ValueError

                request.user.username = username
                request.user.email = email
                request.user.bio = bio
                request.user.save()

                if profile:
                    profile.age = age
                    profile.height = height
                    profile.weight = weight
                    profile.gender = gender
                    profile.goal = goal
                    profile.food_preferences = food_preferences
                    profile.allergies = allergies
                    profile.save()

                else:
                    NutritionProfile.objects.create(user=request.user,age=age,height=height,weight=weight,gender=gender, goal=goal, food_preferences=food_preferences, allergies=allergies)
                return redirect("profile")

            except (ValueError, TypeError):
                error = "Please enter valid profile information."

        elif action == "delete":
            NutritionProfile.objects.filter(user=request.user ).delete()
            return redirect("profile")

    profile = NutritionProfile.objects.filter(user=request.user).first()

    return render(request, "profile.html", { "profile": profile,  "error": error})