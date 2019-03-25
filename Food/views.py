from typing import Dict, List, Optional, Union
import json
from django.db.models.query import QuerySet
from django.core import serializers
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from Food.models import Product


class JsonSearch(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if request.content_type != 'application/json':
            return JsonResponse([], safe=False)
        query: Dict[str, str] = json.loads(request.body)
        search: Optional[str] = query.get('food_search')
        if search is None:
            return JsonResponse([], safe=False)
        product: Optional[Product] = self._find_product(search)
        if not product:
            return JsonResponse([], safe=False)
        return HttpResponse(serializers.serialize(
            'json', self._find_substitutes(product)
        ), content_type='application/json')

    def _find_product(self, product_name: str) -> Optional[Product]:
        products: QuerySet = Product.objects.filter(name=product_name)
        if products:
            return products.first()  # Should only exist ONE product w/ this name # noqa

    def _find_substitutes(self, product: Product) -> QuerySet:
        return Product.get_substitutes_for(product).all()

    def substitute_product(
        self, search: Optional[str]
    ) -> Union[QuerySet, List[Product]]:
        if search is not None:
            product: Optional[Product] = self._find_product(search)
            if product is not None:
                return self._find_substitutes(product)
        return []


class SearchView(View):
    products_list_template: str = 'Food/products.html'

    def post(self, request: HttpRequest) -> HttpResponse:
        search: Optional[str] = request.POST.get('food_search')
        substitutes: List[Product] = []
        if search is not None:
            json_search: JsonSearch = JsonSearch()
            substitutes = json_search.substitute_product(search)
        return render(request, self.products_list_template, locals())
