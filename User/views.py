from typing import Any, Optional, Type
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView, View
from .forms import SignUpForm
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


class SignUpView(CreateView):
    model: Type[User] = User
    template_name: str = 'signup.html'
    form_class: Type[SignUpForm] = SignUpForm
    success_url: str = 'login'

    def form_valid(self, form: Any) -> Any:
        valid = super(SignUpView, self).form_valid(form)
        ...
        # TO CONTINUE, SEE : https://stackoverflow.com/a/31491942
