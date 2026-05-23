from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Service, Review, CallRequest, FAQ
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('telephone', 'email', 'surname', 'name', 'patronymic', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('telephone', 'email', 'name', 'surname')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('telephone', 'email', 'password')}),
        ('Персональная информация', {'fields': ('name', 'surname', 'patronymic', 'birth_date', 'image')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('telephone', 'email', 'name', 'surname', 'password1', 'password2'),
        }),
    )
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'date', 'description')
    list_filter = ('date', 'service')
    search_fields = ('user__name', 'user__surname', 'description')
@admin.register(CallRequest)
class CallRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'telephone', 'service', 'created_at', 'processed')
    list_filter = ('processed', 'created_at')
    search_fields = ('name', 'telephone')
    actions = ['mark_as_processed']
    def mark_as_processed(self, request, queryset):
        queryset.update(processed=True)
    mark_as_processed.short_description = "Отметить как обработанные"
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)
    ordering = ('order',)