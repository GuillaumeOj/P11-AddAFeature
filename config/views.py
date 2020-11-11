from urllib.parse import quote

from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from django.template import loader
from django.views.decorators.csrf import requires_csrf_token

from product.forms import ProductSearchForm


@requires_csrf_token
def custom_bad_request(request, exception):
    """Custom page for 400 errors"""

    product_search_form = ProductSearchForm()

    context = {
        "product_search_form": product_search_form,
    }

    template = loader.get_template("400.html")
    body = template.render(context, request)

    return HttpResponseBadRequest(body)


@requires_csrf_token
def custom_permission_denied(request, exception):
    """Custom page for 403 errors"""

    product_search_form = ProductSearchForm()

    context = {
        "product_search_form": product_search_form,
    }

    template = loader.get_template("403.html")
    body = template.render(context, request)

    return HttpResponseForbidden(body)


@requires_csrf_token
def custom_page_not_found(request, exception):
    """Custom page for 404 errors"""
    exception_repr = exception.__class__.__name__

    try:
        message = exception.args[0]
    except (AttributeError, IndexError):
        pass
    else:
        if isinstance(message, str):
            exception_repr = message

    product_search_form = ProductSearchForm()

    context = {
        "request_path": quote(request.path),
        "exception": exception_repr,
        "product_search_form": product_search_form,
    }

    template = loader.get_template("404.html")
    body = template.render(context, request)

    return HttpResponseNotFound(body, content_type=None)


@requires_csrf_token
def custom_server_error(request):
    """Custom page for 500 errors"""

    product_search_form = ProductSearchForm()

    context = {
        "product_search_form": product_search_form,
    }

    template = loader.get_template("500.html")
    body = template.render(context, request)

    return HttpResponseServerError(body)
