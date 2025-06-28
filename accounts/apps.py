from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    def ready(self):
        post_migrate.connect(create_user_groups,sender=self)

def create_user_groups(sender,**kwargs):
    from django.contrib.auth.models import Group
    Group.objects.get_or_create(name='Manager')
    Group.objects.get_or_create(name='Customer')