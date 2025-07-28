from django.contrib import admin
from .models import Menu, MenuItem

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "menu", "parent", "order", "url", "named_url")
    list_filter = ("menu",)
    search_fields = ("title", "url", "named_url")
    ordering = ("menu", "parent", "order")
