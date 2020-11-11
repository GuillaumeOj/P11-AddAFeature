from django.urls import path

from . import views

app_name = "search"
urlpatterns = [
    path("", views.get_product, name="get_product"),
    path("auto_find/", views.auto_completion, name="auto_completion"),
    path("<str:product_code>/", views.get_substitutes, name="get_substitutes"),
    path(
        "<str:product_code>/<str:page>/", views.get_substitutes, name="get_substitutes"
    ),
]
