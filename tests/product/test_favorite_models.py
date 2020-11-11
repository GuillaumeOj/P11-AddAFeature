from product.models import Favorite, Product
from tests.custom import CustomTestCase


class FavoriteModelsTests(CustomTestCase):
    def setUp(self):
        self.product = Product.objects.filter(name="Nutella").first()
        self.substitute = Product.objects.filter(
            name="Pâte À Tartiner Chocolat Noisette"
        ).first()

    def test_category_printing_name(self):
        favorite = Favorite.objects.create(
            product=self.product, substitute=self.substitute
        )

        self.assertIsInstance(favorite, Favorite)
        self.assertEqual(
            favorite.__str__(),
            f"Produit : {favorite.product} / Substitut : {favorite.substitute}",
        )

    def test_create_favorite(self):
        favorite = Favorite.objects.create(
            product=self.product, substitute=self.substitute
        )

        self.assertIsInstance(favorite, Favorite)
        self.assertEqual(favorite.product, self.product)
        self.assertEqual(favorite.substitute, self.substitute)
        self.assertIs(favorite.full_clean(), None)

    def test_create_favorite_with_no_substitute(self):
        with self.assertRaises(ValueError):
            Favorite.objects.create(product=self.product, substitute="")

    def test_create_favorite_with_no_product(self):
        with self.assertRaises(ValueError):
            Favorite.objects.create(product="", substitute=self.substitute)
