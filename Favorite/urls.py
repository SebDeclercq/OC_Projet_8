from typing import List
from django.urls import path
from django.utils.translation import gettext as _
from . import views


app_name: str = 'favorite'


urlpatterns: List[path] = [
    path(_('save'), views.SaveView.as_view(), name=_('save')),
]
