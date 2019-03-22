from typing import List
from django.urls import path
from django.utils.translation import gettext as _
from . import views


app_name: str = 'food'


urlpatterns: List[path] = [
    path(_('search_json'), views.JsonSearch.as_view(), name=_('search_json')),
]