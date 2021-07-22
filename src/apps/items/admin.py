from django.contrib import admin
from .models import Categories, Items, Unit


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_from')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('categories', 'name', 'item_img', 'price', 'description', 'create_at', 'update_at')

class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_at', 'update_at')

admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Items, ItemAdmin)
admin.site.register(Unit, UnitAdmin)
