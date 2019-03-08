from typing import Any, Optional
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, View
from .models import User


class LoginView(TemplateView):
    template_name: str = 'login.html'

    def post(
            self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        email: Optional[str] = request.POST.get('email')
        password: Optional[str] = request.POST.get('password')
        user: Optional[User] = authenticate(  # type: ignore
            username=email, password=password
        )
        if user is not None and user.is_active:
            login(request, user)
            return render(request, self.template_name)
        return render(request, self.template_name, {'wrong_credentials': True})


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return redirect('user:login')
