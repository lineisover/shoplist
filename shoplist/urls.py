from django.urls import path
from . import views

app_name = "shoplist"

urlpatterns = [
    path('space/<int:space_id>/lists/', views.shoppinglist, name='shoppinglist'),
    path('list/<int:list_id>/items/', views.item_list, name='item_list'),
    path('item/<int:pk>/toggle/', views.toggle_item, name='toggle_item'),
    path('new_space_form/', views.new_space_form, name='new_space_form'),
    path("space/create/", views.create_space, name="create_space"),
    path("space/<int:pk>/delete/", views.delete_space, name="delete_space"),
]
