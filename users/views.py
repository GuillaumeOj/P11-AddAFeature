from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from product.forms import ProductSearchForm

from .forms import UserLoginForm, UserRegistrationForm

User = get_user_model()


def custom_login_view(request):
    product_search_form = ProductSearchForm()
    context = {"product_search_form": product_search_form}

    # Get the next view url
    redirect_to = request.POST.get("next", request.GET.get("next", "homepage:index"))
    if redirect_to:
        context["next"] = redirect_to

    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        email = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            success_message = f"Bonjour {user.first_name} !"
            messages.success(request, success_message)
            return redirect(redirect_to)
        else:
            fail_message = "Vos identifiants sont incorrects."
            messages.error(request, fail_message)
            return redirect(reverse("users:login"))
    else:
        login_form = UserLoginForm()

    context["login_form"] = login_form
    return render(request, "users/login.html", context=context)


def custom_logout_view(request):
    success_message = f"Au revoir {request.user.first_name}"
    messages.success(request, success_message)

    redirect_to = request.POST.get("next", request.GET.get("next", "homepage:index"))

    logout(request)

    return redirect(redirect_to)


def registration(request):
    """Register a user."""
    product_search_form = ProductSearchForm()
    context = {"product_search_form": product_search_form}

    redirect_to = request.POST.get("next", request.GET.get("next", "homepage:index"))
    if redirect_to:
        context["next"] = redirect_to

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            user = User.objects.create_user(
                email=email,
                first_name=first_name,
                password=password,
                last_name=last_name,
            )
            user.save()
            success_message = f"Bienvenue parmis nous {first_name} !"
            messages.success(request, success_message)
            return redirect(redirect_to)
    else:
        form = UserRegistrationForm()

    context["form"] = form
    return render(request, "users/registration.html", context=context)


@login_required
def account(request):
    """User account details."""
    product_search_form = ProductSearchForm()
    context = {"product_search_form": product_search_form}

    redirect_to = request.POST.get("next", request.GET.get("next", "homepage:index"))
    if redirect_to:
        context["next"] = redirect_to

    return render(request, "users/account.html", context=context)
