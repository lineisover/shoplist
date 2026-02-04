from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from .models import UserSpace, ShopList, Item
from .forms import UserSpaceForm

@login_required
def home(request):
    """Главная страница возвращает все пространства пользователя"""
    spaces = request.user.space.all()  # связка User → UserSpace через related_name
    return render(request,
                  "shoplist/home.html",
                  {"spaces": spaces, 
                   "title": "Твои пространства"})

@login_required
def shoppinglist(request, space_id):
    """Возвращает все списки в указанном пространстве"""
    space = get_object_or_404(UserSpace, id=space_id)
    shoppinglists = space.lists.all()
    return render(request, "shoplist/shoppinglist.html", {"shoppinglists": shoppinglists, "space": space})

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

def new_space_form(request):
    form = UserSpaceForm()
    return render(request, "shoplist/partials/new_space_form.html", {"form": form})

@require_POST
def create_space(request):
    form = UserSpaceForm(request.POST)
    if form.is_valid():
        space = form.save()
        # Добавляем текущего пользователя в ManyToMany
        space.users.add(request.user)
        return render(request, "shoplist/partials/space_item.html", {"space": space})
    # Если форма невалидна, возвращаем её с ошибками
    return render(request, "shoplist/partials/new_space_form.html", {"form": form})

@require_http_methods(["DELETE"])
def delete_space(request, pk):
    try:
        space = UserSpace.objects.get(id=pk)
        # Опционально: проверяем, что request.user является участником
        if request.user in space.users.all():
            space.delete()
            return HttpResponse("")  # пустой ответ, htmx удаляет li
        else:
            return HttpResponse("Forbidden", status=403)
    except UserSpace.DoesNotExist:
        return HttpResponse("Not found", status=404)
