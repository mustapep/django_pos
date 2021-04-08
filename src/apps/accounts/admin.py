from django.contrib import admin
from .models import Sales, CardMembers, Members


class SalsesProfile(admin.ModelAdmin):
    list_display = ('user', 'address', 'nik_numb', 'create_at', 'update_at')


class MemberAdmin(admin.ModelAdmin):
    list_display = ('customers', 'gender', 'photo', 'create_at', 'update_at')


class CardMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_at', 'update_at')


admin.site.register(Sales, SalsesProfile)
admin.site.register(Members, MemberAdmin)
admin.site.register(CardMembers, CardMemberAdmin)
