from django.test import TestCase
from django.urls import reverse

from mount.models import Mount, Category


class MountTestCase(TestCase):
    fixtures = ["mount.fixture.json", "mount_category.fixture.json"]

    def test_list_mounts(self):
        responce = self.client.get(
            reverse('home'),
        )
        self.assertEqual(responce.status_code, 200)
        mounts_list = Category.objects.all()
        mounts_in_context = responce.context["posts"]
        self.assertEqual(len(mounts_list), len(mounts_in_context))
