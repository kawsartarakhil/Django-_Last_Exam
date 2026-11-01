from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers  import CustomUserManager
import uuid 

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)

    objects = CustomUserManager()


class NutritionProfile(models.Model):

    gender = [('male', 'Male'),('female', 'Female'),]
    goal = [('lose', 'Lose weight'),('maintain', 'Maintain weight'),('gain', 'Gain weight'),]
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='nutrition_profile')
    age = models.PositiveIntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    gender = models.CharField(max_length=10, choices=gender)
    goal = models.CharField(max_length=10, choices=goal)
    food_preferences = models.TextField(blank=True)
    allergies = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class EmailConfirmation(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    token = models.UUIDField(default = uuid.uuid4)
 