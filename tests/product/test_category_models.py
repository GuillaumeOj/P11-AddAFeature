from django.core.exceptions import ValidationError
from django.db.utils import DataError

from product.models import Category
from tests.custom import CustomTestCase


class CategoryModelsTests(CustomTestCase):
    def setUp(self):
        self.category = Category.objects.all().first()

    def test_category_printing_name(self):
        category = self.category

        self.assertIsInstance(category, Category)
        self.assertEqual(category.__str__(), category.name)

    def test_create_category(self):
        category = Category.objects.create(name="Test")

        self.assertIsInstance(category, Category)
        self.assertEqual(category.name, "Test")
        self.assertIs(category.full_clean(), None)

    def test_create_category_with_name_too_short(self):
        category = Category.objects.create(name="T")

        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_create_category_with_name_too_long(self):

        with self.assertRaises(DataError):
            Category.objects.create(name=101 * "T")
