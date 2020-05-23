from django.contrib.auth import authenticate, login


def login_user(user, request):
    user = authenticate(username=user.username, password=user.passwor)
    if user is not None:
        if user.is_active:
            request.session.set_expiry(86400)  # sets the exp. value of the session
            login(request, user)
