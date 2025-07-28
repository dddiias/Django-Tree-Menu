from typing import Dict, List, Optional
from django import template
from django.urls import reverse, NoReverseMatch
from ..models import MenuItem

register = template.Library()

def _resolve_item_url(item: dict) -> Optional[str]:
    """Преобразуем named_url в реальный путь (reverse) либо берём явный url."""
    if item.get("named_url"):
        try:
            return reverse(item["named_url"])
        except NoReverseMatch:
            return None
    return item.get("url")

def _build_tree(items: List[dict]) -> dict:
    """Собираем дерево в памяти: индексы по parent_id и id."""
    by_parent: Dict[Optional[int], List[dict]] = {}
    by_id: Dict[int, dict] = {}
    for it in items:
        it["children"] = []
        it["is_active"] = False
        it["is_open"] = False
        by_id[it["id"]] = it
        by_parent.setdefault(it["parent_id"], []).append(it)

    for it in items:
        it["children"] = by_parent.get(it["id"], [])

    return {"by_parent": by_parent, "by_id": by_id}

def _norm(p: Optional[str]) -> Optional[str]:
    if not p:
        return None
    return p if p.endswith("/") else p + "/"

def _find_active_id(items: List[dict], req_path: str) -> Optional[int]:
    """Сопоставляем текущий путь с URL пунктов меню."""
    rp = _norm(req_path)
    for it in items:
        target = _norm(_resolve_item_url(it))
        if target and target == rp:
            return it["id"]
    return None

def _open_branch(by_id: dict, active_id: Optional[int]) -> None:
    """Отмечаем активную ветку: все предки открыты, активный узел помечен."""
    cur = by_id.get(active_id) if active_id else None
    while cur:
        cur["is_open"] = True
        cur["is_active"] = (cur["id"] == active_id)
        parent_id = cur.get("parent_id")
        cur = by_id.get(parent_id)

@register.inclusion_tag("menu/tree.html", takes_context=True)
def draw_menu(context, menu_name: str):
    request = context.get("request")

    items = list(
        MenuItem.objects
        .filter(menu__name=menu_name)
        .values("id", "parent_id", "title", "order", "url", "named_url")
        .order_by("order", "id")
    )

    tree = _build_tree(items)
    active_id = _find_active_id(items, request.path if request else "")
    _open_branch(tree["by_id"], active_id)

    if active_id:
        node = tree["by_id"][active_id]
        for ch in node.get("children", []):
            ch["is_open"] = True

    return {"roots": tree["by_parent"].get(None, [])}
