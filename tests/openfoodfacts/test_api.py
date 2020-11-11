from unittest.mock import patch

from django.test import TestCase
from requests import ConnectionError, HTTPError, Timeout

from openfoodfacts.api import Api


class MockRequestsResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code == 200:
            return True
        elif self.status_code in [404, 500]:
            raise HTTPError
        elif self.status_code == 408:
            raise Timeout
        else:
            raise ConnectionError


class MockRequests:
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

    def get(self, *args, **kwargs):
        return MockRequestsResponse(self.data, self.status_code)


class ApiTests(TestCase):
    def test_api_return_products(self):
        data = {
            "products": [
                {
                    "nutriscore_grade": "d",
                    "code": "7622210449283",
                    "url": "https://fr.openfoodfacts.org/produit/chocolat-au-ble-complet",
                    "product_name": "Prince goût chocolat au blé complet",
                }
            ]
        }
        mock_requests_get = MockRequests(data, 200).get

        mock_pages = 1

        with patch("openfoodfacts.api.Api.PAGES", mock_pages):
            with patch("openfoodfacts.api.requests.get", mock_requests_get):
                products = Api().get_products()

                self.assertEqual(products, data["products"])

    def test_api_with_no_connection(self):
        data = {
            "products": [
                {
                    "nutriscore_grade": "d",
                    "code": "7622210449283",
                    "url": "https://fr.openfoodfacts.org/produit/chocolat-au-ble-complet",
                    "product_name": "Prince goût chocolat au blé complet",
                }
            ]
        }
        mock_requests_get = MockRequests(data, "").get

        with patch("openfoodfacts.api.requests.get", mock_requests_get):
            with self.assertRaises(ConnectionError):
                Api().get_products()

    def test_api_with_timeout(self):
        data = {
            "products": [
                {
                    "nutriscore_grade": "d",
                    "code": "7622210449283",
                    "url": "https://fr.openfoodfacts.org/produit/chocolat-au-ble-complet",
                    "product_name": "Prince goût chocolat au blé complet",
                }
            ]
        }
        mock_requests_get = MockRequests(data, 408).get

        with patch("openfoodfacts.api.requests.get", mock_requests_get):
            with self.assertRaises(Timeout):
                Api().get_products()

    def test_api_with_not_found_error(self):
        data = {
            "products": [
                {
                    "nutriscore_grade": "d",
                    "code": "7622210449283",
                    "url": "https://fr.openfoodfacts.org/produit/chocolat-au-ble-complet",
                    "product_name": "Prince goût chocolat au blé complet",
                }
            ]
        }
        mock_requests_get = MockRequests(data, 404).get

        with patch("openfoodfacts.api.requests.get", mock_requests_get):
            with self.assertRaises(HTTPError):
                Api().get_products()

    def test_api_with_internal_server_error(self):
        data = {
            "products": [
                {
                    "nutriscore_grade": "d",
                    "code": "7622210449283",
                    "url": "https://fr.openfoodfacts.org/produit/chocolat-au-ble-complet",
                    "product_name": "Prince goût chocolat au blé complet",
                }
            ]
        }
        mock_requests_get = MockRequests(data, 500).get

        with patch("openfoodfacts.api.requests.get", mock_requests_get):
            with self.assertRaises(HTTPError):
                Api().get_products()
