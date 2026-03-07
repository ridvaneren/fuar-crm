from django.urls import path
from .views import (
    dashboard,
    CompanyListView,
    CompanyCreateView,
    CompanyUpdateView,
    CompanyDeleteView,
    FairListView,
    FairCreateView,
    FairUpdateView,
    FairDeleteView,
    import_excel_view,
    export_companies_excel,
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('companies/add/', CompanyCreateView.as_view(), name='company_add'),
    path('companies/<int:pk>/edit/', CompanyUpdateView.as_view(), name='company_edit'),
    path('companies/<int:pk>/delete/', CompanyDeleteView.as_view(), name='company_delete'),
    path('fairs/', FairListView.as_view(), name='fair_list'),
    path('fairs/add/', FairCreateView.as_view(), name='fair_add'),
    path('fairs/<int:pk>/edit/', FairUpdateView.as_view(), name='fair_edit'),
    path('fairs/<int:pk>/delete/', FairDeleteView.as_view(), name='fair_delete'),
    path('import/', import_excel_view, name='import_excel'),
    path('export/', export_companies_excel, name='export_excel'),
]
