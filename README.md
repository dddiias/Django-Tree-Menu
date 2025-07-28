# Django Tree Menu

Древовидное меню на Django, которое:
- хранится в БД (модели `Menu`, `MenuItem`) и редактируется в стандартной админке;
- рендерится **template‑тегом** `{% draw_menu 'имя' %}`;
- раскрывает **всю цепочку предков активного пункта** и **первый уровень его потомков**;
- поддерживает **несколько меню на одной странице**;
- делает **ровно 1 SQL‑запрос** на отрисовку **каждого** меню.

## Требования
- Python 3.11+ (OK и с 3.12/3.13)
- Django 5.x
- База: SQLite (по умолчанию)

## Установка и запуск

```bash
# 1) Клонирование
git clone https://github.com/dddiias/Django-Tree-Menu DjangoTreeMenu
cd DjangoTreeMenu

# 2) Виртуальное окружение
python -m venv .venv
# Windows PowerShell:
. .venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# 3) Зависимости
pip install -r requirements.txt

# 4) Миграции и суперпользователь
python manage.py migrate
python manage.py createsuperuser

# 5) (Опционально) демо‑данные
python manage.py loaddata demo_menu.json

# 6) Запуск
python manage.py runserver
```

## Тестирование 
Запуск:
```bash
python manage.py test -v 2
```
Покрыто: **один запрос** на рендер меню, **подсветка активного**, **раскрытие дочерних узлов**.