
from django.http import HttpResponseRedirect
from django.urls import reverse

def guest_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dashboard'))  # Redirect to dashboard if authenticated
        return view_func(request, *args, **kwargs)
    return _wrapped_view
