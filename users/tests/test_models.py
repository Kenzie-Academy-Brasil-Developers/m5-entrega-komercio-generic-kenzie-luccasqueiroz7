from django.test import TestCase
from users.models import User
from products.models import Product


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = {
            "username": "luccas",
            "first_name": "luccas",
            "last_name": "queiroz",
            "is_seller": False,
        }

        cls.product = {
            "description": "batata frita",
            "price": 22.99,
            "quantity": 3,
            "is_active": True,
        }

        cls.user_created = User.objects.create(**cls.user)
        cls.products_created = [
            Product.objects.create(**cls.product, seller=cls.user_created)
            for _ in range(10)
        ]

    def test_username_unique(self):
        unique = self.user_created._meta.get_field("username").unique

        self.assertEqual(unique, True)

    def test_first_name_max_length(self):
        max_length = self.user_created._meta.get_field("first_name").max_length

        self.assertEqual(max_length, 150)

    def test_last_name_max_length(self):
        max_length = self.user_created._meta.get_field("last_name").max_length

        self.assertEqual(max_length, 50)

    def test_is_seller_null_blank(self):
        nullable = self.user_created._meta.get_field("is_seller").null
        blankable = self.user_created._meta.get_field("is_seller").blank

        self.assertTrue(nullable)
        self.assertTrue(blankable)

    def test_one_to_many_users_products(self):

        for product in self.products_created:
            self.assertIn(product, self.user_created.products.all())
