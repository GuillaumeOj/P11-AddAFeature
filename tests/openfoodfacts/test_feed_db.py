from django.test import TestCase

from openfoodfacts.feed_db import FeedDb
from product.models import Category, Product


class FeedDbTests(TestCase):
    def test_insert_product_with_all_required_fields(self):
        data = [
            {
                "nutriscore_grade": "d",
                "code": "7622210449283",
                "url": "https://fr.openfoodfacts.org/produit/chocolat-au-ble-complet-lu",
                "product_name": "Prince goût chocolat au blé complet",
            }
        ]
        feeder = FeedDb()
        feeder.feed_db(data)
        product = Product.objects.filter(code="7622210449283")

        self.assertTrue(product)

    def test_insert_product_without_a_nutriscore_grade(self):
        data = [
            {
                "code": "7622210449283",
                "url": "https://fr.openfoodfacts.org/produit/chocolat-au-ble-complet-lu",
                "product_name": "Prince goût chocolat au blé complet",
            }
        ]
        feeder = FeedDb()
        feeder.feed_db(data)
        product = Product.objects.filter(code="7622210449283")

        self.assertFalse(product)

    def test_insert_product_without_a_code(self):
        data = [
            {
                "nutriscore_grade": "d",
                "url": "https://fr.openfoodfacts.org/produit/chocolat-au-ble-complet-lu",
                "product_name": "Prince goût chocolat au blé complet",
            }
        ]
        feeder = FeedDb()
        feeder.feed_db(data)
        product = Product.objects.filter(nutriscore_grade="d")

        self.assertFalse(product)

    def test_insert_product_without_an_url(self):
        data = [
            {
                "nutriscore_grade": "d",
                "code": "7622210449283",
                "product_name": "Prince goût chocolat au blé complet",
            }
        ]
        feeder = FeedDb()
        feeder.feed_db(data)
        product = Product.objects.filter(code="7622210449283")

        self.assertFalse(product)

    def test_insert_product_with_a_nutriscore_too_long(self):
        data = [
            {
                "nutriscore_grade": "de",
                "code": "7622210449283",
                "url": "https://fr.openfoodfacts.org/produit/chocolat-au-ble-complet-lu",
                "product_name": "Prince goût chocolat au blé complet",
            }
        ]
        feeder = FeedDb()
        feeder.feed_db(data)
        product = Product.objects.filter(code="7622210449283")

        self.assertFalse(product)

    def test_insert_product_with_a_code_too_long(self):
        data = [
            {
                "nutriscore_grade": "d",
                "code": "76222104492834",
                "url": "https://fr.openfoodfacts.org/produit/chocolat-au-ble-complet-lu",
                "product_name": "Prince goût chocolat au blé complet",
            }
        ]
        feeder = FeedDb()
        feeder.feed_db(data)
        product = Product.objects.filter(code="76222104492834")

        self.assertFalse(product)

    def test_insert_product_with_a_code_too_short(self):
        data = [
            {
                "nutriscore_grade": "d",
                "code": "762221044928",
                "url": "https://fr.openfoodfacts.org/produit/chocolat-au-ble-complet-lu",
                "product_name": "Prince goût chocolat au blé complet",
            }
        ]
        feeder = FeedDb()
        feeder.feed_db(data)
        product = Product.objects.filter(code="762221044928")

        self.assertFalse(product)

    def test_insert_product_with_a_category_name_too_long(self):
        data = [
            {
                "nutriscore_grade": "d",
                "code": "7622210449283",
                "url": "https://fr.openfoodfacts.org/produit/chocolat-au-ble-complet-lu",
                "product_name": "Prince goût chocolat au blé complet",
                "categories": 105 * "a",
            }
        ]
        feeder = FeedDb()
        feeder.feed_db(data)
        categories = Category.objects.all()
        product = Product.objects.filter(code="7622210449283")

        self.assertFalse(categories)
        self.assertTrue(product)

    def test_insert_product_with_categories(self):
        data = [
            {
                "nutriscore_grade": "d",
                "code": "7622210449283",
                "url": "https://fr.openfoodfacts.org/produit/chocolat-au-ble-complet-lu",
                "product_name": "Prince goût chocolat au blé complet",
                "categories": "foo,bar",
            }
        ]
        feeder = FeedDb()
        feeder.feed_db(data)
        categories = Category.objects.all()
        product = Product.objects.all().first()

        self.assertTrue(categories)
        self.assertTrue(len(categories) == 2)
        self.assertTrue(product)
        self.assertTrue(len(product.categories.all()) == 2)
