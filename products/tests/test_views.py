from rest_framework.test import APITestCase
from products.models import Product
from users.models import User

from rest_framework.authtoken.models import Token


class ProductsViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.product = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15,
        }

        cls.product_negative_quantity = {
            "description": "Iphone 10",
            "price": 1000.99,
            "quantity": -5,
        }

        cls.admin = {
            "username": "luccas",
            "password": "1234",
            "first_name": "luccas",
            "last_name": "queiroz",
            "is_seller": False,
        }

        cls.seller = {
            "username": "anna",
            "password": "1234",
            "first_name": "anna",
            "last_name": "cristinna",
            "is_seller": True,
        }

        cls.seller_2 = {
            "username": "zilda",
            "password": "1234",
            "first_name": "zilda",
            "last_name": "queiroz",
            "is_seller": True,
        }

        cls.not_seller = {
            "username": "rute",
            "password": "1234",
            "first_name": "rute",
            "last_name": "queiroz",
            "is_seller": False,
        }

        cls.login_admin = {
            "username": "luccas",
            "password": "1234",
        }

        cls.login_seller = {
            "username": "anna",
            "password": "1234",
        }

        cls.login_seller_2 = {
            "username": "zilda",
            "password": "1234",
        }

        cls.login_not_seller = {
            "username": "rute",
            "password": "1234",
        }

        cls.account_admin = User.objects.create_superuser(**cls.admin)
        cls.account_seller = User.objects.create_user(**cls.seller)
        cls.account_seller_2 = User.objects.create_user(**cls.seller_2)
        cls.account_not_seller = User.objects.create_user(**cls.not_seller)

    def test_creation_product_seller(self):
        token = self.client.post(
            "/api/login/",
            self.login_seller,
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["token"])

        response = self.client.post(
            "/api/products/",
            self.product,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)

    def test_creation_product_not_seller(self):
        token = self.client.post(
            "/api/login/",
            self.login_not_seller,
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["token"])

        response = self.client.post(
            "/api/products/",
            self.product,
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_update_product_owner_seller(self):
        product = Product.objects.create(
            **self.product,
            seller=self.account_seller,
        )

        token = self.client.post(
            "/api/login/",
            self.login_seller,
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["token"])

        response = self.client.patch(
            f"/api/products/{product.id}/",
            {"description": "Iphone 13"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["description"], "Iphone 13")

    def test_update_product_not_owner_seller(self):
        product = Product.objects.create(
            **self.product,
            seller=self.account_seller,
        )

        token = self.client.post(
            "/api/login/",
            self.login_not_seller,
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["token"])

        response = self.client.patch(
            f"/api/products/{product.id}/",
            {"description": "Iphone 13"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_list_products(self):
        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)

    def test_specific_return_creation_product(self):
        token = self.client.post(
            "/api/login/",
            self.login_seller,
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["token"])

        response = self.client.post(
            "/api/products/",
            self.product,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)
        self.assertIn("seller", response.data)
        self.assertIn("description", response.data)
        self.assertIn("price", response.data)
        self.assertIn("quantity", response.data)
        self.assertIn("is_active", response.data)

    def test_specific_return_list_products(self):
        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)

    def test_creation_product_missing_keys(self):
        token = self.client.post(
            "/api/login/",
            self.login_seller,
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["token"])

        response = self.client.post(
            "/api/products/",
            {},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.data,
            {
                "description": ["This field is required."],
                "price": ["This field is required."],
                "quantity": ["This field is required."],
            },
        )

    def test_creation_product_negative_quantity(self):
        token = self.client.post(
            "/api/login/",
            self.login_seller,
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["token"])

        response = self.client.post(
            "/api/products/",
            self.product_negative_quantity,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.data,
            {
                "quantity": ["Ensure this value is greater than or equal to 0."],
            },
        )
