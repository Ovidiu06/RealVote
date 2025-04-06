from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from django.utils.dateparse import parse_datetime
from django.contrib.auth import logout
from django.shortcuts import redirect


class SessionTimeoutMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.logout_time = getattr(settings, 'SESSION_TIMEOUT_MINUTES', 5)

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.session is not None:
                last_activity_time = request.session.get('session_timeout_last_active')
                current_time = now()
                if last_activity_time:
                    last_activity_time = parse_datetime(last_activity_time)
                    if last_activity_time:
                        inactive_duration = (current_time - last_activity_time).total_seconds() / 60
                        if inactive_duration > self.logout_time:
                            logout(request)
                            return redirect('login')
                request.session['session_timeout_last_active'] = current_time.isoformat()
        response = self.get_response(request)
        return response

class RedirectMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path == '/':
            return HttpResponseRedirect(reverse('voting:dashboard'))
        return self.get_response(request)


class Redirect404ToLoginMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 404:
            return redirect('login')
        return response