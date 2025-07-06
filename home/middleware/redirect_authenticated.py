from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse('login-page')
        register_url = reverse('register-page')  # You must have this URL name defined

        # Check if user is authenticated and trying to access login or register
        if request.user.is_authenticated and request.path in [login_url, register_url]:
            return redirect('dashboard-page')  # Or wherever you want to redirect them

        return self.get_response(request)
