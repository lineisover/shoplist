from django.contrib import admin
from .models import Item, ShopList, UserSpace


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    fields = ('name', 'done',)
    readonly_fields = ()


@admin.register(UserSpace)
class UserSpaceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('users',)
    

@admin.register(ShopList)
class ShopListAdmin(admin.ModelAdmin):
    list_display = ('name', 'space')
    inlines = [ItemInline]
    
    
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'shopping_list', 'done')
    list_filter = ('done',)