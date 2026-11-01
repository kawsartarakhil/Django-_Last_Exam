from django.conf import settings
from django.db import models


class RecipeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    

class Recipe(models.Model):
    MEAL_TYPES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snacks"),
    ]
    CATEGORIES = [
        ("weight_gain", "Weight Gain"),
        ("muscle_support", "Muscle Support"),
        ("balanced", "Balanced Nutrition"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="recipes/")
    ingredients = models.TextField()
    instructions = models.TextField()
    calories = models.IntegerField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)
    carbs = models.FloatField(blank=True, null=True)
    fat = models.FloatField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES, blank=True)
    nutrition_category = models.CharField(max_length=20, choices=CATEGORIES, blank=True)

    class Meta:
        permissions = [
            ("can_manage_recipes", "Can manage recipes"),
            ("can_feature_recipes", "Can feature recipes"),
            ("can_view_all_recipes", "Can view all recipes"),
        ]

    def __str__(self):
        return self.title

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = RecipeManager()
    all_objects = models.Manager()

    def delete(self):
        from django.utils import timezone

        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        super().delete()

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="favorites")
    recipe = models.ForeignKey("Recipe",on_delete=models.CASCADE,related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "recipe")

    def __str__(self):
        return f"{self.user} - {self.recipe}"


class GroceryItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="grocery_items")
    name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=100, blank=True)
    is_purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MealSuggestion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="meal_suggestions")
    ingredients_entered = models.TextField()
    recipe = models.ForeignKey("Recipe",on_delete=models.CASCADE,null=True,blank=True,related_name="suggestions")
    generated_recipe = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion for {self.user}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject