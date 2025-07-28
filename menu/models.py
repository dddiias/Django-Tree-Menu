from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint

class Menu(models.Model):
    name = models.CharField("Название", max_length=64, unique=True)
    slug = models.SlugField("Слаг", max_length=64, unique=True)

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items", verbose_name="Меню")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
                               related_name="children", verbose_name="Родитель")

    title = models.CharField("Заголовок", max_length=128)
    order = models.PositiveIntegerField("Порядок", default=0)

    url = models.CharField("URL", max_length=256, null=True, blank=True)
    named_url = models.CharField("Named URL", max_length=128, null=True, blank=True)

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            CheckConstraint(
                check=(
                    (Q(url__isnull=False) & ~Q(url="") & Q(named_url__isnull=True)) |
                    (Q(named_url__isnull=False) & ~Q(named_url="") & Q(url__isnull=True))
                ),
                name="menuitem_exactly_one_link_set",
            ),
            UniqueConstraint(fields=["menu", "parent", "title"],
                             name="menuitem_unique_siblings_title"),
        ]
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

    def __str__(self):
        return self.title

    def clean(self):
        seen = set()
        p = self.parent
        while p is not None:
            if p.pk == self.pk:
                raise ValidationError("Циклы в дереве запрещены.")
            if p.pk in seen:
                raise ValidationError("Обнаружен цикл в дереве.")
            seen.add(p.pk)
            p = p.parent
