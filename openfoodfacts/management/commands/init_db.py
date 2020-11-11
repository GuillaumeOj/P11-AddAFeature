from django.core.management import BaseCommand
from requests import ConnectionError, HTTPError, Timeout

from openfoodfacts.api import Api
from openfoodfacts.feed_db import FeedDb


class Command(BaseCommand):
    help = "Initialize the database with products from OpenFoodFacts"

    def handle(self, *args, **options):
        self.stdout.write("Downloading products from OpenFoodFacts")
        api = Api()
        try:
            raw_products = api.get_products()
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
            self.stdout.write(self.style.SUCCESS("Done."))

            self.stdout.write("Inserting products in the database")
            feeder = FeedDb()
            if feeder.feed_db(raw_products):
                self.stdout.write(self.style.SUCCESS("Done."))
            else:
                self.stdout.write(
                    self.style.error("Could'nt insert products in the database.")
                )
