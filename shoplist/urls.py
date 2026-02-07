from django.urls import path
from . import views

app_name = "shoplist"

urlpatterns = [
    path("space/create/", views.create_space, name="create_space"),
    path("space/<int:space_id>/delete/", views.delete_space, name="delete_space"),
    path('space/<int:space_id>/lists/', views.shoppinglist, name='shoppinglist'),
    path("space/<int:space_id>/add-user/", views.add_user_to_space, name="add_user_to_space"),
    path("space/<int:space_id>/add-user-form/", views.show_add_user_form, name="show_add_user_form"),
    path("space/<int:space_id>/<int:user_id>/", views.remove_user_from_space, name="remove_user_from_space"),
    path('list/<int:list_id>/items/', views.item_list, name='item_list'),
    path('item/<int:pk>/toggle/', views.toggle_item, name='toggle_item'),
    path('new_space_form/', views.new_space_form, name='new_space_form'),
]
