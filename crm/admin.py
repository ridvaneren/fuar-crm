from django.contrib import admin
from .models import Fair, Company


@admin.register(Fair)
class FairAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'start_date', 'end_date')
    search_fields = ('name', 'city', 'country', 'organizer')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'authorized_person', 'phone', 'email', 'company_status', 'next_action', 'fair')
    search_fields = ('company_name', 'authorized_person', 'phone', 'email', 'website')
    list_filter = ('company_status', 'next_action', 'fair')
