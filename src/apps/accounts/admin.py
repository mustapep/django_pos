from django.contrib import admin
from .models import Employee, CardMember, Member


class EmployeeProfile(admin.ModelAdmin):
    list_display = ('user', 'address', 'nik_numb', 'create_at', 'update_at')


class MemberAdmin(admin.ModelAdmin):
    list_display = ('customers', 'gender', 'photo', 'create_at', 'update_at')


class CardMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_at', 'update_at')


admin.site.register(Employee, EmployeeProfile)
admin.site.register(Member, MemberAdmin)
admin.site.register(CardMember, CardMemberAdmin)
