from django.urls import path
from .views import *

urlpatterns = [
    path("", home_view, name="home"),
    path("recipes/", recipes_view, name="recipes"),
    path("about/", about_view, name="about"),
    path("dashboard/",dashboard_view,name="dashboard"),
    path("meal_suggestions",meal_suggestions_view,name="meal_suggestions"),
    path("grocery-list/",grocery_list_view, name="grocery_list"),
    path("recipes/<int:recipe_id>/favorite/",favorite_toggle_view, name="favorite_toggle"),
    path("favorites/",favorites_view,name="favorites"),
    path("profile/",profile_view, name="profile"),
]