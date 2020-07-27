from django.shortcuts import reverse
from django.test import override_settings

from product.models import Product
from tests.custom import CustomTestCase


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class SearchViewsAutoFindTests(CustomTestCase):
    def get_nutella(self):
        return Product.objects.filter(name="Nutella").first()

    def test_auto_find_return_json(self):
        url = reverse("search:auto_find")
        response = self.client.post(url, data={"name": "nut"})

        self.assertEqual(response.status_code, 200)

    def test_auto_find_return_no_json_if_for_is_invalid(self):
        url = reverse("search:auto_find")
        response = self.client.post(url, data={"name": ""})

        self.assertEqual(response.status_code, 400)

    def test_auto_find_redirect_if_accessing_with_get(self):
        url = reverse("search:auto_find")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class SearchViewsFindProductTests(CustomTestCase):
    def get_nutella(self):
        return Product.objects.filter(name="Nutella").first()

    def test_find_product_redirect_to_find_substitutes(self):
        url = reverse("search:find")
        response = self.client.post(url, data={"name": "Nutella"})

        self.assertEqual(response.status_code, 200)

    def test_find_product_render_substites_if_product_not_found(self):
        url = reverse("search:find")
        response = self.client.post(url, data={"name": "qwerty"})

        self.assertEqual(response.status_code, 200)

    def test_find_product_redirect_if_accessing_with_get(self):
        url = reverse("search:find")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_find_substitutes_is_loading_with_correct_product(self):
        nutella = self.get_nutella()
        url = reverse("search:find_substitutes", args=[nutella.code])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_find_substitutes_is_loading_with_wrong_product_code(self):
        url = reverse("search:find_substitutes", args=["wrong_code"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_find_substitutes_is_loading_with_page_number_is_not_integer(self):
        nutella = self.get_nutella()
        url = reverse("search:find_substitutes", args=[nutella.code, "wrong_page_number"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_find_substitutes_is_loading_with_wrong_page_number(self):
        nutella = self.get_nutella()
        url = reverse("search:find_substitutes", args=[nutella.code, 150])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
