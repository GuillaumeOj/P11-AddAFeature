from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render, reverse

from homepage.custom_http_response import HttpResponseBadRequest
from product.forms import ProductSearchForm
from product.models import Product


def auto_completion(request):
    """Get a list of products' names for the auto-completion.

    :return: a JsonResponse with a list of products' name, if succed to get products
    an HttpResponseBadRequest if the form is not valid
    an HttpResponse with a redirection to home if acces with another method than POST
    :rtype: JsonResponse
    """

    if request.method == "POST":
        form = ProductSearchForm(request.POST)

        if form.is_valid():
            # Get a list of products and create a list of names
            products = Product.objects.get_products_by_name(form["name"].value())
            products_names = [product.name for product in products]
            products_names = list(set(products_names))

            # Create a response as a dict for returning a JsonResponse
            response = {"products_names": products_names}
            return JsonResponse(response)
        else:
            return HttpResponseBadRequest()

    # Avoid reach the view by the GET method and redirect to the index
    return redirect(reverse("homepage:index"))


def get_product(request):
    """Get a product to substitute based on the user search terms.

    :return: an HttpResponse with a redirection to substitutes if succeed to get a product
    an HttpResponse with a template render if fail to get a product
    an HttpResponse with a redirection to home if acces with another method than POST
    :rtype: HttpResponse
    """

    if request.method == "POST":
        product_search_form = ProductSearchForm(request.POST)
        context = {"product_search_form": product_search_form}

        if product_search_form.is_valid():
            # Get the product by using the name
            product = Product.objects.get_product_by_name(
                product_search_form.cleaned_data["name"]
            )

            # Redirect to the method find_substitutes if the product exist
            if product:
                return redirect(reverse("search:get_substitutes", args=[product.code]))
            # Else render the substitute page without substitutes
            else:
                context["product"] = {"name": product_search_form.cleaned_data["name"]}
                return render(request, "search/substitutes.html", context=context)

    # Avoid reach the view by the GET method and redirect to the index
    return redirect(reverse("homepage:index"))


def get_substitutes(request, product_code, page=""):
    """Get a list of substitutes for a product.

    :return: an HttpResponse with a template render for displaying the subsitutes
    :rtype: HttpResponse
    """

    product_search_form = ProductSearchForm()
    context = {"product_search_form": product_search_form}

    product = Product.objects.get_product_by_code(product_code)

    if product:
        context["product"] = product
        substitutes = Product.objects.find_substitutes(product.code)

        if substitutes:
            # Paginate the subsitutes result
            pagination = Paginator(substitutes, 6, orphans=3)
            try:
                context["substitutes"] = pagination.page(page)
            except PageNotAnInteger:
                context["substitutes"] = pagination.page(1)
            except EmptyPage:
                context["substitutes"] = pagination.page(pagination.num_pages)

    return render(request, "search/substitutes.html", context=context)
