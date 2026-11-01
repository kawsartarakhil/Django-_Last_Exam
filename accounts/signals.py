from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Recipe


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name != 'accounts':
        return

    Group.objects.get_or_create(name='User')

    nutritionist, created = Group.objects.get_or_create(name='Nutritionist')

    content_type = ContentType.objects.get_for_model(Recipe)

    permissions = Permission.objects.filter(
        content_type=content_type,
        codename__in=['add_recipe', 'change_recipe', 'delete_recipe','view_recipe','can_feature_recipes','can_view_all_recipes','can_manage_recipes',]
    )

    nutritionist.permissions.set(permissions)