from django.urls import path

from . import views

app_name = "product"
urlpatterns = [
    path("sheet/<str:product_code>/", views.sheet, name="sheet"),
    path(
        "save/<str:product_code>/<str:substitute_code>/",
        views.save_favorite,
        name="save",
    ),
    path("favorites/", views.favorites, name="favorites"),
]
