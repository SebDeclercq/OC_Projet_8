from typing import Dict, List, Optional
import json
from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse
# from django.shortcuts import render
from django.views.generic import View
from Food.models import Product


class JsonSearch(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        print(f'>>>>>>>>>>>\n\n{request.text}\n\n<<<<<<<<<<<<')
        if not request.content_type('application/json'):
            return JsonResponse([], safe=False)
        query: Dict[str, str] = json.loads(request.content)
        if 'food_search' not in query:
            return JsonResponse([], safe=False)
        product: Optional[Product] = self._find_product(query['food_search'])
        if not product:
            return JsonResponse([], safe=False)
        return JsonResponse(json.dumps(
            self._find_substitutes(product)
        ), safe=False)

    def _find_product(self, product_name: str) -> Optional[Product]:
        products: QuerySet = Product.objects.filter(name=product_name)
        if products:
            return products.first()  # Should only exist ONE product w/ this name # noqa

    def _find_substitutes(self, product: Product) -> List[str]:
        substitutes: List[str] = []
        for product in Product.get_substitutes_for(product).all():
            substitutes.append(product.to_json)
        return substitutes
