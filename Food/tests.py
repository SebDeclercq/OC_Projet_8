from typing import Dict, Optional
from django.test import TestCase
from .models import Product


class TestProductModel(TestCase):
    def setUp(self) -> None:
        self.data: Dict[str, str] = dict(
            barcode='123456', name='Test product',
            nutrition_grade='A', url='http://example.com',
        )

    def test_product_insertion(self) -> None:
        product: Product = Product.objects.create(**self.data)
        self.assertEqual(Product.objects.first(), product)

    def test_product_repr(self) -> None:
        Product.objects.create(**self.data)
        product: Optional[Product] = Product.objects.first()
        if product is not None:
            self.assertEqual(
                str(product),
                f'<Product#{self.data["barcode"]} name={self.data["name"]} '
                f'nutrition_grade={self.data["nutrition_grade"]}'
            )
