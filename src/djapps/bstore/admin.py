from django.contrib import admin

from .models import Block, Currency, Provider


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = [
        'currency',
        'provider',
        'block_number',
        'block_created_at',
        'created_at',
    ]
    search_fields = ['currency__name', 'provider__name']
    list_filter = ['currency', 'provider']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
