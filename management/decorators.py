from accounts.models import CustomUser

def is_manager(user):
    return user.groups.filter(name="Manager").exists()