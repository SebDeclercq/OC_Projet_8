from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.test import Client, TestCase
from User.models import User
from Food.models import Category, Product
from .models import Favorite


class TestFavorites(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            email='az@er.ty', password='azerty'
        )
        self.bad_product: Product = Product.objects.create(
            barcode='789123', name='Test product 2',
            nutrition_grade='C', url='http://example2.com',
        )
        self.good_product: Product = Product.objects.create(
            barcode='123456', name='Test product',
            nutrition_grade='A', url='http://example.com',
        )
        self.catego: Category = Category.objects.create(name='Category 1')
        self.catego.products.add(self.bad_product)
        self.catego.products.add(self.good_product)

    def test_insert_new_favorite(self) -> None:
        favorite: Favorite = Favorite.objects.create(
            substituted=self.bad_product,
            substitute=self.good_product,
            user=self.user
        )
        self.assertEqual(Favorite.objects.first(), favorite)

    def test_double_insert_rejected(self) -> None:
        with self.assertRaises(IntegrityError):
            for i in range(2):
                Favorite.objects.create(
                    substituted=self.bad_product,
                    substitute=self.good_product,
                    user=self.user
                )

    def test_multiple_users_same_favorite(self) -> None:
        Favorite.objects.create(
            substituted=self.bad_product,
            substitute=self.good_product,
            user=self.user
        )
        Favorite.objects.create(
            substituted=self.bad_product,
            substitute=self.good_product,
            user=User.objects.create(email='qw@er.ty', password='qwerty')
        )
        self.assertEqual(len(Favorite.objects.filter(user=self.user)), 1)


class TestFavoriteView(TestCase):
    URL: str = '/favorite/save'

    def setUp(self) -> None:
        self.email: str = 'az@er.ty'
        self.password: str = 'azerty'
        self.user: User = User.objects.create_user(
            email=self.email, password=self.password
        )
        self.bad_product: Product = Product.objects.create(
            barcode='789123', name='Test product 2',
            nutrition_grade='C', url='http://example2.com',
        )
        self.good_product: Product = Product.objects.create(
            barcode='123456', name='Test product',
            nutrition_grade='A', url='http://example.com',
        )
        self.catego: Category = Category.objects.create(name='Category 1')
        self.catego.products.add(self.bad_product)
        self.catego.products.add(self.good_product)

    def test_insert_new_favorite(self) -> None:
        self.client.login(username=self.email, password=self.password)
        self.client.post(self.URL, {
            'substituted': self.bad_product.barcode,
            'substitute': self.good_product.barcode
        })
        self.assertEqual(Favorite.objects.filter(user=self.user).count(), 1)

    def test_insert_new_favorite_response(self) -> None:
        self.client.login(username=self.email, password=self.password)
        response: HttpResponse = self.client.post(self.URL, {
            'substituted': self.bad_product.barcode,
            'substitute': self.good_product.barcode
        })
        self.assertJSONEqual(response.content.decode('utf-8'), {
            'status': 'success', 'substitute': self.good_product.barcode,
            'substituted': self.bad_product.barcode
        })

    def test_insert_new_favorite_no_user(self) -> None:
        response: HttpResponse = self.client.post(self.URL, {
            'substituted': self.bad_product.barcode,
            'substitute': self.good_product.barcode
        })
        self.assertJSONEqual(response.content.decode('utf-8'), {
            'status': 'error'
        })


class FavoriteListViewTest(TestCase):
    URL: str = '/favorite/list'

    def setUp(self) -> None:
        self.email: str = 'az@er.ty'
        self.password: str = 'azerty'
        self.user: User = User.objects.create_user(
            email=self.email, password=self.password
        )
        self.bad_product: Product = Product.objects.create(
            barcode='789123', name='Test product 2',
            nutrition_grade='C', url='http://example2.com',
        )
        self.good_product: Product = Product.objects.create(
            barcode='123456', name='Test product',
            nutrition_grade='A', url='http://example.com',
        )
        self.favorite: Favorite = Favorite.objects.create(
            substituted=self.bad_product,
            substitute=self.good_product,
            user=self.user
        )

    def test_favorites_list_template(self) -> None:
        self.client.login(username=self.email, password=self.password)
        response: HttpResponse = self.client.get(self.URL)
        self.assertTemplateUsed(response, 'Favorite/list.html')

    def test_no_user(self) -> None:
        response: HttpResponse = self.client.get(self.URL)
        self.assertRedirects(response, '/user/login')
