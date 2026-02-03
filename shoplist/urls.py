from django.urls import path
from . import views

app_name = "shoplist"

urlpatterns = [
    path('space/<int:space_id>/lists/', views.shoppinglist_list, name='shoppinglist_list'),
    path('list/<int:list_id>/items/', views.item_list, name='item_list'),
    path('item/<int:pk>/toggle/', views.toggle_item, name='toggle_item'),
]
