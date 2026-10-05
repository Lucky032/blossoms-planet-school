from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def allowed_roles(*allowed_roles):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("login")

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            profile = getattr(request.user, "userprofile", None)

            if profile and profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            messages.error(
                request,
                "You don't have permission to access this page.",
            )

            return redirect("dashboard")

        return wrapper

    return decorator