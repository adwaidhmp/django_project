from django.shortcuts import redirect
from django.contrib import messages

class BlockAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        path = request.path

        # URLs to allow admins on student side
        allowed_for_admin = ['/logout/', '/']  # add other public student URLs if needed

        # Admin block to access student pages
        if (request.user.is_staff or request.user.is_superuser) and not path.startswith('/adm/'):
            if path not in allowed_for_admin:
                return redirect('/adm/')

        # Student bloc to access admin pages
        if not (request.user.is_staff or request.user.is_superuser) and path.startswith('/adm/'):
            return redirect('/')  # Redirect to student home

        return self.get_response(request)



