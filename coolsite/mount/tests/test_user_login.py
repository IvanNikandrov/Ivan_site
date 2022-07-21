from django.contrib.auth.forms import UserModel
from django.test import TestCase
from django.urls import reverse


class UserLoginTestCase(TestCase):
    @classmethod
    def setUp(self):
        password = 'qwerty123'
        self.user = UserModel.objects.create_user(
            "john",
            "john@ex.com",
            password
        )
        self.password = password

    def test_user_login(self):
        response = self.client.post(
            reverse("login"),
            data={
                "username": self.user.username,
                "password": self.password
            }
        )
        self.assertEqual(response.url, reverse("home"))

    def test_access_to_protected_page(self):

        self.client.login(username=self.user.username, password=self.password)

        response = self.client.get(
            reverse("add_page"),
        )
        self.assertFalse(response.context["user"].is_anonymous)

        self.assertEqual(response.status_code, 200)
