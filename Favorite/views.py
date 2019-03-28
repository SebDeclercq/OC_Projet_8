from django.core import serializers
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from Favorite.models import Favorite
from Food.models import Product
from User.models import User


class SaveView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        user: User = request.user  # type: ignore
        if user.is_authenticated:
            substituted: QuerySet = Product.objects.filter(
                barcode=request.POST.get('substituted')
            )
            substitute: QuerySet = Product.objects.filter(
                barcode=request.POST.get('substitute')
            )
            Favorite.objects.create(
                user=user,
                substituted=substituted.first(),
                substitute=substitute.first()
            )
            return JsonResponse({
                'status': 'success',
                'substitute': serializers.serialize('json', substitute)[1:-1],  # type: ignore # noqa
                'substituted': serializers.serialize('json', substituted)[1:-1]  # type: ignore # noqa
            })
        return JsonResponse({'status': 'error'})


class FavoriteListView(View):
    favorites_list_template: str = 'Favorite/list.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        user: User = request.user  # type: ignore
        if user.is_authenticated:
            favorites: QuerySet = Favorite.objects.filter(
                user=user
            ).all()
            return render(request, self.favorites_list_template, {
                'favorites': favorites
            })
        else:
            return redirect(reverse('user:login'))
