from typing import List
from django.urls import path
from django.utils.translation import gettext as _
from . import views


app_name: str = 'user'


urlpatterns: List[path] = [
    path(_('login'), views.LoginView.as_view(), name=_('login')),
    path(_('logout'), views.LogoutView.as_view(), name=_('logout')),
]
