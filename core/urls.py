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
    path("contact/", contact_view, name="contact"),
    path("recipes/<int:pk>/",recipe_detail_view, name="recipe_detail"),
    path('recipes/create/', create_recipe_view, name='create_recipe'),
    path('recipes/<int:id>/update/', update_recipe_view, name='update_recipe'),
    path('recipes/<int:id>/delete/', delete_recipe_view, name='delete_recipe'),
    path('recipes/<int:id>/restore/', restore_recipe_view, name='restore_recipe'),
    path('recipes/<int:id>/hard-delete/', hard_delete_recipe_view, name='hard_delete_recipe'),
    path('recipes/deleted/', deleted_recipes_view, name='deleted_recipes'),
]