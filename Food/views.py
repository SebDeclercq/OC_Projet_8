from typing import Dict, List, Optional, Union
import json
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from Food.models import Product
from User.models import User
from Favorite.models import Favorite


class SearchView(View):
    products_list_template: str = 'Food/products.html'

    def post(self, request: HttpRequest) -> HttpResponse:
        search: Optional[str] = request.POST.get('food_search')
        substitutes: List[Product] = []
        if search is not None:
            substituted, substitutes = self.substitute_product(search)  # type: ignore  # noqa
        return render(request, self.products_list_template, locals())

    def _find_product(self, product_name: str) -> Optional[Product]:
        products: QuerySet = Product.objects.filter(name=product_name)
        if products:
            return products.first()  # Should only exist ONE product w/ this name # noqa

    def _find_substitutes(self, product: Product) -> QuerySet:
        return Product.get_substitutes_for(product).all()

    def substitute_product(
        self, search: Optional[str]
    ) -> Union[QuerySet, List[None]]:
        if search is not None:
            product: Optional[Product] = self._find_product(search)
            if product is not None:
                return product, self._find_substitutes(product)
        return [None, None]


class ProductView(View):
    product_details_template: str = 'Food/details.html'

    def get(
        self, request: HttpRequest, substitute_barcode: str,
        substituted_barcode: str
    ) -> HttpResponse:
        substitute: Optional[Product] = Product.objects.filter(
            barcode=substitute_barcode
        ).first()
        substituted: Optional[Product] = Product.objects.filter(
            barcode=substituted_barcode
        ).first()
        user: User = request.user  # type: ignore
        if user.is_authenticated:
            if Favorite.objects.filter(user=user, substitute=substitute):
                is_favorite: bool = True
            else:
                is_favorite = False
        return render(request, self.product_details_template, locals())


class AjaxView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        results: List[str] = []
        query: str = request.GET.get('term', '')
        for r in Product.objects.filter(name__icontains=query):
            results.append(r.name)
        return JsonResponse(results, safe=False)
