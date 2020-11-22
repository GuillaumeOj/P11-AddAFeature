import logging
import smtplib

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from django.template import loader

from .forms import ProductSearchForm
from .models import Favorite, Product


logger = logging.getlogger(__name__)


def sheet(request, product_code):
    """Display the detail sheet for a product.

    :param product_code: the code for the product to display
    :type product_code: str
    :return: an HttpResponse with a template and context dictionnary the product exist
    an HttpResponseNotFound if the product doesn't exist
    :rtype: HttpResponse
    """
    product_search_form = ProductSearchForm()
    context = {
        "product_search_form": product_search_form,
    }

    redirect_to = request.POST.get("next", request.GET.get("next", "homepage:index"))
    if redirect_to:
        context["next"] = redirect_to

    product = Product.objects.get_product_by_code(product_code)
    if product:
        context["product"] = product
        return render(request, "product/sheet.html", context=context)

    return HttpResponseNotFound()


@login_required
def save_favorite(request, product_code, substitute_code):
    """Save a substitute in favorites for the current user.

    :param product_code: the code for the substituted product
    :type product_code: str
    :param substitute_code: the code for the substitute
    :type substitute_code: str
    :return: redirect to the previous page
    :rtype: HttpResponseRedirect
    """
    product = Product.objects.get_product_by_code(product_code)
    substitute = Product.objects.get_product_by_code(substitute_code)

    redirect_to = request.POST.get("next", request.GET.get("next", "homepage:index"))

    if product and substitute:
        current_user = request.user

        favorite, created = Favorite.objects.get_or_create(
            product=product, substitute=substitute
        )
        if favorite not in current_user.favorites.all():
            current_user.favorites.add(favorite)
            success_message = f"{substitute.name} est sauvegardé dans vos favoris"
            messages.success(request, success_message)
        else:
            s_name = substitute.name
            p_name = product.name
            error_message = (
                f"{s_name} est déjà dans vos favoris pour substituer {p_name}"
            )
            messages.error(request, error_message)

        return redirect(redirect_to)
    else:
        return HttpResponseNotFound()


@login_required
def favorites(request):
    """Display all favorites for the current user.

    :return: an HttpResponse with a template and context dictionnary
    :rtype: HttpResponse
    """
    product_search_form = ProductSearchForm()
    context = {
        "product_search_form": product_search_form,
    }
    favorites = request.user.favorites.order_by("-product")
    context["favorites"] = favorites

    return render(request, "product/favorites.html", context=context)


@require_http_methods(["POST"])
@login_required
def send_product_sheet_by_email(request):
    """Send a product sheet by email to the current user.

    Expect an input value with the code of the product to send by e-mail.
    :return: redirect to the previous page
    :rtype: HttpResponseRedirect
    """

    if request.POST:
        product = Product.objects.get_product_by_code(request.POST.get("product_code"))
        redirect_to = request.POST.get("next")

        if product:
            subject = f"Pur Beurre - Votre fiche pour {product.name}"
            to = [request.user.email]

            context = {
                "user": request.user,
                "product": request.product,
                "sheet_url": request.sheet_url,
            }

            text_content = loader.render_to_string("emails/sheet_text.html", context)
            html_content = loader.render_to_string("emails/sheet.mjml", context)

            try:
                send_mail(subject, text_content, None, to, html_message=html_content)
                messages.success("Votre fiche est envoyée !")
            except smtplib.SMTPException as e:
                error = e.strerror
                error += f"Could'nt send email (subject: {subject}, to: {to[0]})"
                logger.error(error)

                messages.error(
                    "Une erreur s'est produite. Votre fiche n'a pas était envoyée."
                )

            return redirect(redirect_to)

    return HttpResponseNotFound()
