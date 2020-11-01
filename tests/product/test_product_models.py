from django.core.exceptions import ValidationError
from django.db.utils import DataError

from product.models import Product
from tests.custom import CustomTestCase


class ProductModelsTests(CustomTestCase):
    def setUp(self):
        self.product = Product.objects.all().first()

    def test_product_printing_name(self):
        product = self.product

        self.assertIsInstance(product, Product)
        self.assertEqual(product.__str__(), f"{product.code} - {product.name}")

    def test_create_product(self):
        product = Product.objects.create(
            code="1234567890987",
            name="Test",
            nutriscore_grade="a",
            url="https://www.foo.bar/",
        )

        self.assertIsInstance(product, Product)
        self.assertEqual(product.name, "Test")
        self.assertIs(product.full_clean(), None)

    def test_create_product_with_name_too_short(self):
        product = Product.objects.create(
            code="1234567890987",
            name="T",
            nutriscore_grade="a",
            url="https://www.foo.bar/",
        )

        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_name_too_long(self):
        with self.assertRaises(DataError):
            Product.objects.create(
                code="1234567890987",
                name=101 * "T",
                nutriscore_grade="a",
                url="https://foo.bar/test/",
            )

    def test_create_product_with_no_name(self):
        product = Product.objects.create(
            code="1234567890987",
            name="",
            nutriscore_grade="a",
            url="https://www.foo.bar/",
        )

        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_code_too_short(self):
        product = Product.objects.create(
            code="123456789098",
            name="Test",
            nutriscore_grade="a",
            url="https://www.foo.bar/",
        )

        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_code_too_long(self):
        with self.assertRaises(DataError):
            Product.objects.create(
                code="12345678909878",
                name="Test",
                nutriscore_grade="a",
                url="https://foo.bar/test/",
            )

    def test_create_product_with_no_code(self):
        product = Product.objects.create(
            code="",
            name="Test",
            nutriscore_grade="a",
            url="https://www.foo.bar/",
        )

        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_wrong_url(self):
        product = Product.objects.create(
            code="1234567890987",
            name="Test",
            nutriscore_grade="a",
            url="https//wwwfoo",
        )

        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_no_url(self):
        product = Product.objects.create(
            code="1234567890987",
            name="Test",
            nutriscore_grade="a",
            url="",
        )

        with self.assertRaises(ValidationError):
            product.full_clean()
