from django.shortcuts import reverse
from django.test import TestCase, override_settings


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class HomepageViewsTests(TestCase):
    def test_index_is_loading(self):
        url = reverse("homepage:index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_disclaimer_is_loading(self):
        url = reverse("homepage:disclaimer")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
