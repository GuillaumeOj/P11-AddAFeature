from progress.bar import IncrementalBar
import requests


class Api:
    """Interface beetween OpenFoodFacts and this application:"""

    # Parameters for the API
    URL_BASE = "https://fr.openfoodfacts.org/cgi/search.pl"
    PAGE_SIZE = 1000
    PAGES = 3
    SORT_BY = "unique_scans_n"
    FIELDS = [
        "code",
        "product_name",
        "url",
        "categories",
        "nutriscore_grade",
        "image_url",
        "image_small_url",
        "nutriments",
    ]

    def get_products(self):
        """Get products from OpenFoodFacts return a list of raw products."""

        parameters = {
            "json": True,
            "action": "process",
            "page_size": self.PAGE_SIZE,
            "sort_by": self.SORT_BY,
            "tagtype_0": "status",
            "tag_contains_0": "without",
            "tag_0": "to-be-completed",
            "tagtype_1": "status",
            "tag_contains_1": "without",
            "tag_1": "to-be-checked",
            "fields": ",".join(self.FIELDS),
        }
        products = list()
        bar = IncrementalBar(
            "Downloading products", max=self.PAGES, suffix="%(percent)d%%"
        )
        bar.start()
        for page in range(self.PAGES):
            parameters["page"] = page
            try:
                response = requests.get(self.URL_BASE, params=parameters)
                response.raise_for_status()
            except requests.HTTPError as err:
                raise err
            except requests.ConnectionError as err:
                raise err
            except requests.Timeout as err:
                raise err

            result = response.json()
            if result.get("products"):
                products.extend(result["products"])
            bar.next()
        bar.finish()

        return products
