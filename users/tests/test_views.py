from rest_framework.test import APITestCase
from users.models import User

from rest_framework.authtoken.models import Token


class UsersViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account_admin = {
            "username": "luccas",
            "password": "1234",
            "first_name": "luccas",
            "last_name": "queiroz",
            "is_seller": False,
        }

        cls.account_seller = {
            "username": "anna",
            "password": "1234",
            "first_name": "anna",
            "last_name": "cristinna",
            "is_seller": True,
        }

        cls.account_not_seller = {
            "username": "rute",
            "password": "1234",
            "first_name": "rute",
            "last_name": "queiroz",
            "is_seller": False,
        }

        cls.login_seller = {
            "username": "anna",
            "password": "1234",
        }

        cls.login_not_seller = {
            "username": "rute",
            "password": "1234",
        }

        cls.updated_account = {
            "username": "zilda",
            "first_name": "zilda",
        }

    def test_creation_account_seller(self):
        response = self.client.post(
            "/api/accounts/",
            self.account_seller,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["is_seller"], True)

    def test_creation_account_not_seller(self):
        response = self.client.post(
            "/api/accounts/",
            self.account_not_seller,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["is_seller"], False)

    def test_creation_account_missing_keys(self):
        response = self.client.post(
            "/api/accounts/",
            {},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.data,
            {
                "username": ["This field is required."],
                "password": ["This field is required."],
                "first_name": ["This field is required."],
                "last_name": ["This field is required."],
            },
        )

    def test_login_seller_token(self):
        create = self.client.post(
            "/api/accounts/",
            self.account_seller,
            format="json",
        )

        response = self.client.post(
            "/api/login/",
            self.login_seller,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_login_not_seller_token(self):
        create = self.client.post(
            "/api/accounts/",
            self.account_not_seller,
            format="json",
        )

        response = self.client.post(
            "/api/login/",
            self.login_not_seller,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_owner_updated_account(self):
        user = User.objects.create_superuser(**self.account_admin)
        token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.patch(
            f"/api/accounts/{user.id}/",
            self.updated_account,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "zilda")
        self.assertEqual(response.data["first_name"], "zilda")

    def test_not_owner_updated_account(self):
        user = User.objects.create_superuser(**self.account_admin)

        create = self.client.post(
            "/api/accounts/",
            self.account_not_seller,
            format="json",
        )
        token = self.client.post(
            "/api/login/",
            self.login_not_seller,
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["token"])

        response = self.client.patch(
            f"/api/accounts/{user.id}/",
            self.updated_account,
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_update_admin_deactivate_account(self):
        user = User.objects.create_superuser(**self.account_admin)
        token = Token.objects.create(user=user)

        create = User.objects.create_user(**self.account_seller)

        id = create.id
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.patch(
            f"/api/accounts/{id}/management/",
            {"is_active": False},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["is_active"], False)

    def test_update_not_admin_deactivate_account(self):
        user = User.objects.create_user(**self.account_seller)
        token = Token.objects.create(user=user)

        create = User.objects.create_user(**self.account_not_seller)
        id = create.id
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.patch(
            f"/api/accounts/{id}/management/",
            {"is_active": False},
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(create.is_active, True)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_update_admin_reactivate_account(self):
        user = User.objects.create_superuser(**self.account_admin)
        token = Token.objects.create(user=user)

        create = User.objects.create_user(**self.account_seller)
        id = create.id
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        deactivate = self.client.patch(
            f"/api/accounts/{id}/management/",
            {"is_active": False},
            format="json",
        )

        response = self.client.patch(
            f"/api/accounts/{id}/management/",
            {"is_active": True},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["is_active"], True)

    def test_list_accounts(self):
        response = self.client.get("/api/accounts/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
