from django.core.exceptions import ObjectDoesNotExist, ValidationError
from progress.bar import IncrementalBar

from product.models import Category, Favorite, Product


class FeedDb:
    """Get products from OpenFoodFacts by using the class Api Normalize the
    data Insert the product and associated categories, brands, stores in the
    database."""

    def feed_db(self, raw_products):

        self._clear_db()

        # Insert each product in the application's database
        bar = IncrementalBar(
            "Inserting products", max=len(raw_products), suffix="%(percent)d%%"
        )
        bar.start()
        for raw_product in raw_products:
            bar.next()
            serialized_product = self._serialize_product(raw_product)

            try:
                product = Product(
                    code=serialized_product["code"],
                    name=serialized_product["name"],
                    url=serialized_product["url"],
                    nutriscore_grade=serialized_product["nutriscore_grade"],
                    image_url=serialized_product["image_url"],
                    image_small_url=serialized_product["image_small_url"],
                    salt_100=serialized_product["salt_100"],
                    sugars_100=serialized_product["sugars_100"],
                    saturated_fat_100=serialized_product["saturated_fat_100"],
                    fat_100=serialized_product["fat_100"],
                )
                product.full_clean()
            except ValidationError:
                # Ignore products with ValidationError
                continue
            product.save()

            # Insert associated categories, stores and brands
            for category in serialized_product["categories"]:
                try:
                    obj = Category.objects.get(name=category)
                except ObjectDoesNotExist:
                    try:
                        obj = Category(name=category)
                        obj.full_clean()
                    except ValidationError:
                        # Ignore categories with ValidationError
                        continue
                    obj.save()

                product.categories.add(obj)
        bar.finish()

        return True

    def _serialize_product(self, raw_product):
        """Serialize a product data informations."""

        def serialize_nutriment(key):
            nutriment_value = nutriments.get(key, 0)
            serialized_nutriment = float(nutriment_value)
            return serialized_nutriment

        serialized = dict()

        serialized["code"] = raw_product.get("code")
        serialized["name"] = raw_product.get("product_name", "").title()
        serialized["url"] = raw_product.get("url", "").lower()
        serialized["nutriscore_grade"] = raw_product.get("nutriscore_grade", "").upper()

        serialized["image_url"] = raw_product.get("image_url", "")
        serialized["image_small_url"] = raw_product.get("image_small_url", "")

        serialized["categories"] = raw_product.get("categories", "").split(",")

        nutriments = raw_product.get("nutriments", {})

        # Transform each nutriment as a float
        serialized["salt_100"] = serialize_nutriment("salt_100g")
        serialized["fat_100"] = serialize_nutriment("fat_100g")
        serialized["saturated_fat_100"] = serialize_nutriment("saturated-fat_100g")
        serialized["sugars_100"] = serialize_nutriment("sugars_100g")

        return serialized

    def _clear_db(self):
        product = Product.objects.all()
        product.delete()

        categories = Category.objects.all()
        categories.delete()

        favorites = Favorite.objects.all()
        favorites.delete()
