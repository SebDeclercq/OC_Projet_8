from typing import Dict, Optional, Union
import json
from django.db.models.query import QuerySet
from django.core import serializers
from django.http import HttpRequest, HttpResponse, JsonResponse
# from django.shortcuts import render
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
        return HttpResponse(self._find_substitutes(product),
                            content_type='application/json')

    def _find_product(self, product_name: str) -> Optional[Product]:
        products: QuerySet = Product.objects.filter(name=product_name)
        if products:
            return products.first()  # Should only exist ONE product w/ this name # noqa

    def _find_substitutes(self, product: Product) -> Union[bytes, str, None]:
        return serializers.serialize(
            'json', Product.get_substitutes_for(product).all()
        )
