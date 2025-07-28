from django.contrib import admin
from django.urls import path
from pages.views import HomeView, AboutView, ContactsView, ProductView, ProductsListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("products/", ProductsListView.as_view(), name="products"),
    path("product/<slug:slug>/", ProductView.as_view(), name="product"),
]
