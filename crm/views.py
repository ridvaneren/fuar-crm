import openpyxl
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import CompanyForm, FairForm, ExcelImportForm
from .models import Company, Fair
from .services import import_companies_from_excel


@login_required
def dashboard(request):
    context = {
        'company_count': Company.objects.count(),
        'fair_count': Fair.objects.count(),
        'teklif_count': Company.objects.filter(company_status='teklif_ver').count(),
        'follow_count': Company.objects.filter(next_action='takip_et').count(),
        'last_companies': Company.objects.select_related('fair').order_by('-created_at')[:8],
    }
    return render(request, 'crm/dashboard.html', context)


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'crm/company_list.html'
    context_object_name = 'companies'
    paginate_by = 20

    def get_queryset(self):
        queryset = Company.objects.select_related('fair', 'owner').all()

        q = self.request.GET.get('q', '').strip()
        status = self.request.GET.get('status', '').strip()
        fair = self.request.GET.get('fair', '').strip()

        if q:
            queryset = queryset.filter(
                Q(company_name__icontains=q) |
                Q(authorized_person__icontains=q) |
                Q(phone__icontains=q) |
                Q(email__icontains=q) |
                Q(website__icontains=q)
            )

        if status:
            queryset = queryset.filter(company_status=status)

        if fair:
            queryset = queryset.filter(fair_id=fair)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fairs'] = Fair.objects.all()
        context['status_choices'] = Company.STATUS_CHOICES
        return context


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'crm/company_form.html'
    success_url = reverse_lazy('company_list')


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'crm/company_form.html'
    success_url = reverse_lazy('company_list')


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'crm/company_confirm_delete.html'
    success_url = reverse_lazy('company_list')


class FairListView(LoginRequiredMixin, ListView):
    model = Fair
    template_name = 'crm/fair_list.html'
    context_object_name = 'fairs'


class FairCreateView(LoginRequiredMixin, CreateView):
    model = Fair
    form_class = FairForm
    template_name = 'crm/fair_form.html'
    success_url = reverse_lazy('fair_list')


class FairUpdateView(LoginRequiredMixin, UpdateView):
    model = Fair
    form_class = FairForm
    template_name = 'crm/fair_form.html'
    success_url = reverse_lazy('fair_list')


class FairDeleteView(LoginRequiredMixin, DeleteView):
    model = Fair
    template_name = 'crm/fair_confirm_delete.html'
    success_url = reverse_lazy('fair_list')


@login_required
def import_excel_view(request):
    if request.method == 'POST':
        form = ExcelImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']
            fair = form.cleaned_data['fair']
            created_count, skipped_count = import_companies_from_excel(
                excel_file,
                fair=fair,
                owner=request.user,
            )
            messages.success(request, f'{created_count} firma aktarıldı. Atlanan satır: {skipped_count}.')
            return redirect('company_list')
    else:
        form = ExcelImportForm()

    return render(request, 'crm/import_excel.html', {'form': form})


@login_required
def export_companies_excel(request):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Firmalar'

    headers = [
        'FirmaID', 'FuarID', 'Firma Adı', 'Yetkili', 'Telefon', 'Eposta',
        'Web', 'Adres', 'Firma Durumu', 'Sonraki Eylem', 'Son Temas', 'Notlar'
    ]
    worksheet.append(headers)

    companies = Company.objects.select_related('fair').all()

    for company in companies:
        worksheet.append([
            company.company_id_code,
            company.fair_id_code,
            company.company_name,
            company.authorized_person,
            company.phone,
            company.email,
            company.website,
            company.address,
            company.company_status,
            company.next_action,
            str(company.last_contact) if company.last_contact else '',
            company.notes,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=firmalar.xlsx'
    workbook.save(response)
    return response
