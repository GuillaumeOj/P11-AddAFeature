from django.core.exceptions import ValidationError

from product.models import Product, Category, Store, Brand


class FeedDb:
    """
    Get products from OpenFoodFacts by using the class Api
    Normalize the data
    Insert the product and associated categories, brands, stores in the database
    """

    def feed_db(self, raw_products):

        self._clear_db()

        # Insert each product in the application's database
        for raw_product in raw_products:
            normalized_product = self._normalize_product(raw_product)

            try:
                product = Product(
                    code=normalized_product["code"],
                    name=normalized_product["name"],
                    url=normalized_product["url"],
                    nutriscore_grade=normalized_product["nutriscore_grade"],
                    generic_name=normalized_product["generic_name"],
                    quantity=normalized_product["quantity"],
                    ingredients_text=normalized_product["ingredients_text"],
                    image_url=normalized_product["image_url"],
                    image_small_url=normalized_product["image_small_url"],
                )
                product.full_clean()
                product.save()
            except ValidationError:
                continue

            # Insert associated categories, stores and brands
            categories = []
            for category in normalized_product["categories"]:
                try:
                    obj, created = Category.objects.get_or_create(name=category)
                    categories.append(obj)
                except ValidationError:
                    continue
            product.categories.add(*categories)

            stores = []
            for store in normalized_product["stores"]:
                try:
                    obj, created = Store.objects.get_or_create(name=store)
                    stores.append(obj)
                except ValidationError:
                    continue
            product.stores.add(*stores)

            brands = []
            for brand in normalized_product["brands"]:
                try:
                    obj, created = Brand.objects.get_or_create(name=brand)
                    brands.append(obj)
                except ValidationError:
                    continue
            product.brands.add(*brands)

    def _normalize_product(self, raw_product):
        """
        Normalize the product data
        """

        normalized = dict()

        normalized["code"] = raw_product.get("code")
        normalized["name"] = raw_product.get("product_name", "").title()
        normalized["url"] = raw_product.get("url", "").lower()
        normalized["nutriscore_grade"] = raw_product.get("nutriscore_grade", "").upper()

        normalized["generic_name"] = raw_product.get("generic_name_fr", "").capitalize()
        normalized["quantity"] = raw_product.get("quantity", "")
        normalized["ingredients_text"] = raw_product.get("ingredients_text", "")

        normalized["image_url"] = raw_product.get("image_url", "")
        normalized["image_small_url"] = raw_product.get("image_small_url", "")

        normalized["categories"] = raw_product.get("categories", "").split(",")
        normalized["stores"] = raw_product.get("stores", "").split(",")
        normalized["brands"] = raw_product.get("brands", "").split(",")

        return normalized

    def _clear_db(self):
        product = Product.objects.all()
        product.delete()

        categories = Category.objects.all()
        categories.delete()

        stores = Store.objects.all()
        stores.delete()

        brands = Brand.objects.all()
        brands.delete()