from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.template.loader import render_to_string
from django.urls import reverse

from account.models import User
from .models import UserSpace, ShopList, Item
from .forms import UserSpaceForm

@login_required
def home(request: HttpRequest) -> HttpResponse:
    """Главная страница возвращает все пространства пользователя"""
    spaces = request.user.space.all()
    return render(request,
                  "shoplist/home.html",
                  {"spaces": spaces, 
                   "title": "Твои пространства"})


@login_required
def shoppinglist(request: HttpRequest, space_id: int) -> HttpResponse:
    """Возвращает все списки в указанном пространстве"""
    space = get_object_or_404(UserSpace, id=space_id)
    shoppinglists = space.lists.all()
    return render(request, "shoplist/shoppinglist.html", {"shoppinglists": shoppinglists, "space": space})


@login_required
def item_list(request: HttpRequest, list_id: int) -> HttpResponse:
    """Возвращает все товары в указанном списке (partial для HTMX)"""
    shopping_list = get_object_or_404(ShopList, id=list_id)
    items = shopping_list.items.all()
    return render(
        request,
        "shoplist/partials/lists/expanded_list.html",
        {
            "items": items,
            "sl": shopping_list
        }
    )
    

@login_required
def hide_item_list(request: HttpRequest, list_id: int) -> HttpResponse:
    """Сворачивает список"""
    shopping_list = get_object_or_404(ShopList, id=list_id)
    items = shopping_list.items.all()
    return render(
        request,
        "shoplist/partials/lists/collapse_list.html",
        {
            "items": items,
            "sl": shopping_list
        }
    )


@login_required
@require_POST
def toggle_item(request: HttpRequest, pk: int) -> HttpResponse:
    item = get_object_or_404(Item, pk=pk)
    sl = item.shopping_list
    
    item.done = not item.done
    item.save()

    return render(request, "shoplist/partials/item_li.html", {"item": item, 'sl': sl})


@login_required
def new_space_form(request: HttpRequest) -> HttpResponse:
    form = UserSpaceForm()
    return render(request, "shoplist/partials/new_space_form.html", {"form": form})


@login_required
@require_POST
def create_space(request: HttpRequest) -> HttpResponse:
    form = UserSpaceForm(request.POST)
    if form.is_valid():
        space = form.save(commit=False)
        space.owner = request.user
        space.save()
        # Добавляем текущего пользователя в ManyToMany
        space.users.add(request.user)
        return render(request, "shoplist/partials/space_item.html", {"space": space})
    # Если форма невалидна, возвращаем её с ошибками
    return render(request, "shoplist/partials/new_space_form.html", {"form": form})


@login_required
@require_http_methods(["DELETE"])
def delete_space(request: HttpRequest, space_id: int) -> HttpResponse:
    space = UserSpace.objects.get(id=space_id)

    if request.user != space.owner:
        return HttpResponse(status=403)
    
    space.delete()
    
    if request.headers.get("HX-Request"):
        return HttpResponse(status=204, headers={"HX-Redirect": reverse("home")})
    
    return HttpResponse("")


@login_required
@require_POST
def add_user_to_space(request: HttpRequest, space_id: int) -> HttpResponse:
    space = get_object_or_404(UserSpace, id=space_id)
    email = request.POST.get('email')
    
    success, message = space.add_user(email, request.user)
    
    return render(
        request,
        "shoplist/partials/space_users_block.html",
        {
            "space": space,
            "error": message if not success else None,
            "success": message if success else None
        }
    )


@login_required
def show_add_user_form(request: HttpRequest, space_id: int) -> HttpResponse:
    space = get_object_or_404(UserSpace, id=space_id)
    return render(request, "shoplist/partials/add_user_form.html", {"space": space})


@login_required
@require_http_methods(["DELETE"])
def remove_user_from_space(request: HttpRequest, space_id: int, user_id: int) -> HttpResponse:
    space = get_object_or_404(UserSpace, id=space_id)
    user = get_object_or_404(User, id=user_id)
    
    success, message = space.remove_user(user)
        
    if request.headers.get('HX-Request'):
        html = render_to_string(
            'shoplist/partials/space_users_block.html',
            {
                'space': space,
                'error': message if not success else None,
                'success': message if success else None
            },
            request=request
        )
        return HttpResponse(html)
    
    
@login_required
def show_add_list_form(request: HttpRequest, space_id: int) -> HttpResponse:
    space = get_object_or_404(UserSpace, id=space_id)
    return render(request, "shoplist/partials/add_list_form.html", {"space": space})


@login_required
def show_add_list_button(request: HttpRequest, space_id: int) -> HttpResponse:
    space = get_object_or_404(UserSpace, id=space_id)
    return render(request, "shoplist/partials/add_list.html", {"space": space})


@login_required
@require_POST
def create_list(request: HttpRequest, space_id: int) -> HttpResponse:
    name = request.POST.get("list_name")
    space = get_object_or_404(UserSpace, id=space_id)
    
    success, message = space.create_list(name)
    
    shoppinglists = ShopList.objects.filter(space=space)
    return render(
        request,
        "shoplist/partials/shoppinglists_container.html",
        {
            "shoppinglists": shoppinglists,
            "space": space,
            'error': message if not success else None,
            'success': message if success else None
        }
    )
    
    
@login_required
@require_POST
def add_item(request: HttpRequest, list_id: int) -> HttpResponse:
    shopping_list = get_object_or_404(ShopList, id=list_id)
    name = request.POST.get("item_name")

    success, message = shopping_list.add_item(name)

    items = shopping_list.items.all()
    
    return render(
        request,
        "shoplist/partials/lists/items_list.html",
        {
            "items": items,
            "sl": shopping_list,
            'error': message if not success else None,
            'success': message if success else None
        }
    )
    
    
@login_required
@require_http_methods(["DELETE"])
def delete_list(request: HttpRequest, list_id: int) -> HttpResponse:
    shopping_list = get_object_or_404(ShopList, id=list_id)
    space = shopping_list.space
    user = request.user

    success, message = space.delete_list(shopping_list, user)

    shoppinglists = space.lists.all()
    
    return render(
        request,
        "shoplist/partials/shoppinglists_container.html",
        {
            "shoppinglists": shoppinglists,
            "space": space,
            'error': message if not success else None,
            'success': message if success else None
        }
    )
    

@login_required
@require_http_methods(["DELETE"])
def delete_item(request: HttpRequest, list_id: int, item_id: int) -> HttpResponse:
    shopping_list = get_object_or_404(ShopList, id=list_id)
    item = get_object_or_404(Item, id=item_id)

    success, message = shopping_list.remove_item(item)

    items = shopping_list.items.all()
    
    return render(
        request,
        "shoplist/partials/lists/items_list.html",
        {
            "items": items,
            "sl": shopping_list,
            'error': message if not success else None,
            'success': message if success else None
        }
    )