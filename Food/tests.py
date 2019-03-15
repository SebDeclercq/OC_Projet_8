from typing import Dict, List, Optional
from django.db.models.query import QuerySet
from django.test import TestCase
from .models import Category, Product


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

    def test_substitute_manager(self) -> None:
        top_product: Product = Product.objects.create(**self.data)
        cat_c_data: Dict[str, str] = dict(
            barcode='789123', name='Test product 2',
            nutrition_grade='C', url='http://example2.com',
        )
        not_so_top_product: Product = Product.objects.create(**cat_c_data)
        substitutes: QuerySet = Product.get_substitutes_for(
            not_so_top_product
        )
        self.assertIn(top_product, substitutes)


class TestCategoryModel(TestCase):
    def test_category_insertion(self) -> None:
        catego: Category = Category.objects.create(name='Category 1')
        self.assertEqual(Category.objects.first(), catego)
