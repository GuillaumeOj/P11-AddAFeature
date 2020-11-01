from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Count
from django.db.models import Q

from .category import Category


class ProductManager(models.Manager):
    """Set custom methods for a product."""

    def get_product_by_code(self, product_code):
        """Get a product with the code.

        :param product_code: the code of the product to get
        :type product_code: str
        :return: a Product if succeed or null
        :rtype: Product
        """
        try:
            product = self.get_queryset().filter(code=product_code).first()
            if not product:
                raise ObjectDoesNotExist()
        except ObjectDoesNotExist:
            product = ""

        return product

    def get_product_by_name(self, name):
        """Get a product with the name.

        Try to get the product by filtering with the exact name, if the query is
        empty, then get the product by filtering with the lookup "__icontains".

        :param name: the name of the product to get
        :type name: str
        :return: a Product if succeed or null
        :rtype: Product
        """
        if name:
            try:
                product = self.get_queryset().filter(name=name).first()
                if not product:
                    raise ObjectDoesNotExist()
            except ObjectDoesNotExist:
                try:
                    product = self.get_queryset().filter(name__icontains=name).first()
                    if not product:
                        raise ObjectDoesNotExist()
                except ObjectDoesNotExist:
                    product = ""
        else:
            product = ""
        return product

    def get_products_by_name(self, name):
        """Get products with the name.

        Get products by filtering with the lookup "__icontains" and limit the results to
        10 products.

        :param name: the name of the product to get
        :type name: str
        :return: a query set with 10 products
        :rtype: QuerySet
        """
        if name:
            try:
                products = self.get_queryset().filter(name__icontains=name)[:10]
                if not products:
                    raise ObjectDoesNotExist()
            except ObjectDoesNotExist:
                products = ""
        else:
            products = ""
        return products

    def find_substitutes(self, product_code):
        """Get substitutes for a product.

        Get the product by using his code.
        Then get substitutes by counting common categories between each products and the
        substituted product. Keep only products with a nutriscore grade lower than the
        substituted product.
        Return a QuerySet order by common categories count (from largest to smallest) and
        nutriscore grade (from lowest-to-highest).

        :param product_code: the code of the product to get
        :type product_code: str
        :return: a query set with 30 substitutes
        :rtype: QuerySet
        """
        product = self.get_product_by_code(product_code)

        if product:
            q = Q(categories__in=product.categories.all()) & Q(
                nutriscore_grade__lt=product.nutriscore_grade
            )
            substitutes = (
                Product.objects.annotate(common_categories=Count("categories", filter=q))
                .order_by("-common_categories", "nutriscore_grade")
                .exclude(code=product.code)
                .exclude(name=product.name)[:30]
            )
            return substitutes


class Product(models.Model):
    """Model for a product."""

    # Required fields
    code = models.CharField(
        max_length=13,
        unique=True,
        validators=[MinLengthValidator(13)],
    )

    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])

    nutriscore_grade = models.CharField(
        max_length=1,
        validators=[MinLengthValidator(1)],
    )

    url = models.URLField()

    # Optionnal fields
    image_url = models.URLField(blank=True)
    image_small_url = models.URLField(
        blank=True,
    )
    fat_100 = models.FloatField(blank=True, default=0)
    saturated_fat_100 = models.FloatField(blank=True, default=0)
    sugars_100 = models.FloatField(blank=True, default=0)
    salt_100 = models.FloatField(blank=True, default=0)

    # Related fields
    categories = models.ManyToManyField(Category)

    # Custom product's manager
    objects = ProductManager()

    class Meta:
        ordering = ["-name", "code"]

    def __str__(self):
        return f"{self.code} - {self.name}"
