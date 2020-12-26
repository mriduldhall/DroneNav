from user_system.models import users


def validate_password(username, password):
    user = users.objects.filter(username=username)
    if (user[0]).password == password:
        return True
    else:
        return False


def change_password(username, password):
    user = users.objects.filter(username=username)
    user = user[0]
    user.password = password
    user.save()
