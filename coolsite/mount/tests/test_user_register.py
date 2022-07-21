from django.contrib.auth.forms import UserModel
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class UserRegisterTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_reg_data = {
            "username": 'john',
            "email": 'john@example.com',
            "password1": '123456789otus',
            "password2": '123456789otus',
        }

    def test_user_register_success(self):
        response = self.client.post(
            reverse('register'),
            data=self.user_reg_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, reverse('home'))
        user = UserModel.objects.get(username=self.user_reg_data["username"])
        self.assertEqual(user.email, self.user_reg_data["email"])
        print(response)

    def test_user_register_username_exists_error(self):
        response = self.client.post(
            reverse('register'),
            data=self.user_reg_data,
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            reverse('register'),
            data=self.user_reg_data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "username",
            _('Пользователь с таким именем уже существует.')
        )

