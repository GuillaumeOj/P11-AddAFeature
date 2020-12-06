from django.core.management import BaseCommand
from requests import ConnectionError, HTTPError, Timeout

from openfoodfacts.api import Api
from openfoodfacts.feed_db import FeedDb


class Command(BaseCommand):
    help = "Initialize the database with products from OpenFoodFacts"

    def handle(self, *args, **options):
        try:
            raw_products = Api().get_products()
        except HTTPError as err:
            if err.status_code == 404:
                self.stdout.write(
                    self.style.http_not_found("Could'nt reach Open Food Facts' API.")
                )
            elif err.status_code == 500:
                message = """Something went wrong with Open Food Facts' servers,
                    please try again later."""

                self.stdout.write(self.style.http_server_error(message))
            else:
                self.stdout.write(
                    self.style.warning("Something went wrong with Open Food Facts'.")
                )
        except ConnectionError:
            self.stdout.write(self.style.WARNING("Please check your connection."))
        except Timeout:
            self.stdout.write(self.style.WARNING("The request timed out."))
        else:
            FeedDb().feed_db(raw_products)
