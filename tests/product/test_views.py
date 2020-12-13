from django.core import mail
from django.shortcuts import reverse
from django.test import Client, override_settings

from product.models import Product
from tests.custom import CustomTestCase
from users.models import User


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class ProductViewsTests(CustomTestCase):
    def setUp(self):
        self.client = Client(HTTP_REFERER="http://www.qwant.fr")
        self.user = User.objects.all().first()

        self.product = Product.objects.filter(name__icontains="nut").first()
        self.substitute = Product.objects.filter(name__icontains="Nocciolata").first()

    def test_sheet_is_loading(self):
        url = reverse("product:sheet", args=[self.product.code])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_sheet_is_not_loading_with_wrong_product_code(self):
        url = reverse("product:sheet", args=["qwerty"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_save_favorite_is_redirecting(self):
        self.client.force_login(self.user)

        url = reverse(
            "product:save",
            kwargs={
                "product_code": self.product.code,
                "substitute_code": self.substitute.code,
            },
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_save_favorite_is_redirecting_if_not_logged(self):
        url = reverse(
            "product:save",
            kwargs={
                "product_code": self.product.code,
                "substitute_code": self.substitute.code,
            },
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_save_favorite_is_redirecting_with_favorite_already_saved(self):
        self.client.force_login(self.user)

        url = reverse(
            "product:save",
            kwargs={
                "product_code": self.product.code,
                "substitute_code": self.substitute.code,
            },
        )
        response = self.client.get(url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_save_favorite_is_not_loading_with_wrong_product_code(self):
        self.client.force_login(self.user)

        url = reverse(
            "product:save",
            kwargs={"product_code": "qwerty", "substitute_code": self.substitute.code},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_save_favorite_is_not_loading_with_wrong_substitute_code(self):
        self.client.force_login(self.user)

        url = reverse(
            "product:save",
            kwargs={"product_code": self.product.code, "substitute_code": "qwerty"},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_favorites_is_loading(self):
        self.client.force_login(self.user)
        url = reverse("product:favorites")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_favorites_is_redirecting_if_not_logged(self):
        url = reverse("product:favorites")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_sheet_by_email(self):
        self.client.force_login(self.user)
        url = reverse("product:sheet_by_email", args=[self.product.code])

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

        messages, _ = response.context["messages"]._get()
        self.assertEqual(str(messages[0]), "Votre fiche est envoyée !")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, "Pur Beurre - Votre fiche pour Nutella Biscuits"
        )
        self.assertEqual(mail.outbox[0].to, ["guillaume.ojardias@gmail.com"])

    def test_sheet_by_email_with_post(self):
        self.client.force_login(self.user)
        url = reverse("product:sheet_by_email", args=[self.product.code])

        response = self.client.post(url, {})

        self.assertEqual(response.status_code, 405)

        self.assertEqual(len(mail.outbox), 0)

    def test_sheet_by_email_without_login(self):
        url = reverse("product:sheet_by_email", args=[self.product.code])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 0)
