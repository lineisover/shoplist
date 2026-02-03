from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserSpace, ShopList, Item

@login_required
def home(request):
    # пример: показываем все пространства пользователя
    spaces = request.user.space.all()  # связка User → UserSpace через related_name
    return render(request, "shoplist/home.html", {"spaces": spaces})

@login_required
def shoppinglist_list(request, space_id):
    """Возвращает все списки в указанном пространстве (partial для HTMX)"""
    space = get_object_or_404(UserSpace, id=space_id)
    shoppinglists = space.lists.all()
    return render(request, "shoplist/shoppinglist_list.html", {"shoppinglists": shoppinglists})

@login_required
def item_list(request, list_id):
    """Возвращает все товары в указанном списке (partial для HTMX)"""
    shopping_list = get_object_or_404(ShopList, id=list_id)
    items = shopping_list.items.all()
    return render(request, "shoplist/item_list.html", {"items": items})

@login_required
def toggle_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    if request.method == "POST":
        item.done = not item.done
        item.save()

    # Возвращаем только один элемент списка (частичный шаблон)
    return render(request, "shoplist/partials/item_li.html", {"item": item})