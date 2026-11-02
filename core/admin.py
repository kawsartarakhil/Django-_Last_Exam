from django.contrib import admin
from .models import Recipe, Favorite, GroceryItem, MealSuggestion


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'meal_type',
        'nutrition_category',
        'calories',
        'is_featured',
        'created_at',
    )

    list_filter = (
        'meal_type',
        'nutrition_category',
        'is_featured',
    )

    search_fields = ('title', 'ingredients')

    list_editable = ('is_featured',)

    ordering = ('-created_at',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'created_at')

    list_filter = ('created_at',)

    search_fields = ('user__username', 'recipe__title')


@admin.register(GroceryItem)
class GroceryItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'user',
        'quantity',
        'is_purchased',
        'created_at',
    )

    list_filter = ('is_purchased', 'created_at')

    search_fields = ('name', 'user__username')

    list_editable = ('is_purchased',)


@admin.register(MealSuggestion)
class MealSuggestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'created_at')

    list_filter = ('created_at',)

    search_fields = ('user__username', 'ingredients_entered')

    ordering = ('-created_at',)
