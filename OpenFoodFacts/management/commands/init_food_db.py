#!/usr/bin/env python3
from typing import Any
import time
from django.core.management.base import (BaseCommand, CommandError,
                                         CommandParser)
from django.db.utils import IntegrityError
from OpenFoodFacts.api import API
from Food.models import Category, Product


class Command(BaseCommand):
    help: str = ('Collects new data from the OpenFoodFacts API '
                 'to populate the Food DB (warning: makes clean slate)')

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--category', action='append', default=[], dest='categories',
            help='List of the expected categories in the Food DB (sep: comma)'
        )
        parser.add_argument(
            '--nb_products', '--nb_products_by_category',
            type=int, dest='nb_products', default=20,
            help='Number of the expected products by category'
        )

    def handle(self, *args: Any, **options: Any) -> None:
        self.api: API = API()
        if not options['categories']:
            raise CommandError('At least one --category is required')
        Category.delete_all()
        Product.delete_all()
        for category_name in options['categories']:
            category: Category = Category.objects.create(name=category_name)
            self.collect_products(category, options['nb_products'])

    def collect_products(self, category: Category, nb_products: int) -> None:
        print(f'Collecting {nb_products} products for "{category.name}"')
        page: int = 1
        while len(category.products.all()) < nb_products:
            self._collect_products(category, page, nb_products)
            page += 1
        print('\n')

    def _collect_products(
        self, category: Category, page: int, nb_products: int
    ) -> None:
        for product in self.api.search(category.name, page, nb_products):
            if len(category.products.all()) >= nb_products:
                break
            try:
                category.products.add(
                    Product.objects.create(**product.to_food_db)
                )
                print('.', end='')
                time.sleep(.2)
            except IntegrityError:
                pass
