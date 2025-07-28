from django.test import TestCase
from django.urls import reverse
from menu.models import Menu, MenuItem

class MenuTagTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        m = Menu.objects.create(name="main", slug="main")
        home = MenuItem.objects.create(menu=m, title="Home", order=1, named_url="home")
        about = MenuItem.objects.create(menu=m, title="About", order=2, named_url="about")
        products = MenuItem.objects.create(menu=m, title="Products", order=3, url="/product/x/")

        MenuItem.objects.create(menu=m, parent=products, title="Product X", order=1, url="/product/x/")
        MenuItem.objects.create(menu=m, parent=products, title="Product Y", order=2, url="/product/y/")

    def test_about_page_renders_menu_with_single_query(self):
        with self.assertNumQueries(1):
            self.client.get(reverse("about"))

    def test_active_node_marked(self):
        res = self.client.get(reverse("about"))
        self.assertContains(res, '<li class="active">', html=False)

    def test_children_of_active_opened(self):
        res = self.client.get(reverse("product", kwargs={"slug": "x"}))
        self.assertContains(res, "Product X")
        self.assertContains(res, "Product Y")
