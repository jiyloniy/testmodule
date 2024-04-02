from django.contrib import admin

from user.models import User
from user.model2 import Company, Student, Teacher



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name',   'phone', 'address', 'user_type']
    list_filter = ['user_type']
    search_fields = ['first_name', 'last_name',   'phone', 'address']
    list_per_page = 10

    fieldsets = (
        ('User Info', {
            'fields': (
            'first_name', 'last_name',   'phone', 'address', 'user_type', 'created_at', 'updated_at', 'user')
        }),
    )
    add_fieldsets = (
        ('User Info', {
            'fields': (
            'first_name', 'last_name',   'phone', 'address', 'user_type', 'user', 'created_at', 'updated_at')
        }),
    )
    ordering = ['id']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    save_on_top = True
    save_as = True

    empty_value_display = '-empty-'


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'logo', 'user', 'created_at', 'updated_at']
    search_fields = ['name', 'location']
    list_per_page = 10

    fieldsets = (
        ('Company Info', {
            'fields': (
                'name', 'location', 'logo', 'user', 'created_at', 'updated_at')
        }),
    )
    add_fieldsets = (
        ('Company Info', {
            'fields': (
                'name', 'location', 'logo', 'user', 'created_at', 'updated_at')
        }),
    )
    ordering = ['id']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    save_on_top = True
    save_as = True

    empty_value_display = '-empty-'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'f_name', 'l_name', 'phone', 'phone_2', 'date_of_birth', 'company', 'created_at', 'updated_at']
    search_fields = ['f_name', 'l_name', 'phone', 'phone_2']
    list_per_page = 10

    fieldsets = (
        ('Student Info', {
            'fields': (
                'f_name', 'l_name', 'phone', 'phone_2', 'date_of_birth', 'company', 'created_at', 'updated_at', 'user')
        }),
    )
    add_fieldsets = (
        ('Student Info', {
            'fields': (
                'f_name', 'l_name', 'phone', 'phone_2', 'date_of_birth', 'company', 'created_at', 'updated_at', 'user')
        }),
    )
    ordering = ['id']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    save_on_top = True
    save_as = True

    empty_value_display = '-empty-'

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'f_name', 'l_name', 'phone', 'phone_2', 'date_of_birth', 'company', 'created_at', 'updated_at']
    search_fields = ['f_name', 'l_name', 'phone', 'phone_2']
    list_per_page = 10

    fieldsets = (
        ('Teacher Info', {
            'fields': (
                'f_name', 'l_name', 'phone', 'phone_2', 'date_of_birth', 'company', 'created_at', 'updated_at', 'user')
        }),
    )
    add_fieldsets = (
        ('Teacher Info', {
            'fields': (
                'f_name', 'l_name', 'phone', 'phone_2', 'date_of_birth', 'company', 'created_at', 'updated_at', 'user')
        }),
    )
    ordering = ['id']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    save_on_top = True
    save_as = True

    empty_value_display = '-empty-'
