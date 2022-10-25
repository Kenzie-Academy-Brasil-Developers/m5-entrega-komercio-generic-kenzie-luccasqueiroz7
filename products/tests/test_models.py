from django.test import TestCase

from products.models import Product
from users.models import User


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.product = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15,
        }

        cls.seller = {
            "username": "anna",
            "password": "1234",
            "first_name": "anna",
            "last_name": "cristinna",
            "is_seller": True,
        }

        cls.account_seller = User.objects.create_user(**cls.seller)
        cls.products_created = [
            Product.objects.create(**cls.product, seller=cls.account_seller)
            for _ in range(10)
        ]

    def test_price_max_digits_decimal_place(self):
        for product in self.products_created:
            max_digits = product._meta.get_field("price").max_digits
            decimal_places = product._meta.get_field("price").decimal_places

            self.assertEqual(max_digits, 10)
            self.assertEqual(decimal_places, 2)

    def test_is_active_null_blank(self):
        for product in self.products_created:

            nullable = product._meta.get_field("is_active").null
            blankable = product._meta.get_field("is_active").blank

            self.assertTrue(nullable)
            self.assertTrue(blankable)

    def test_one_to_many_users_products(self):

        for product in self.products_created:
            self.assertIn(product, self.account_seller.products.all())
