from django import forms
from .models import Company, Fair, Brief


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'fair',
            'owner',
            'company_id_code',
            'fair_id_code',
            'company_name',
            'authorized_person',
            'phone',
            'email',
            'website',
            'address',
            'company_status',
            'next_action',
            'last_contact',
            'notes',
        ]
        widgets = {
            'last_contact': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ['last_contact', 'address', 'notes']:
                field.widget.attrs['class'] = 'form-control'


class FairForm(forms.ModelForm):
    class Meta:
        model = Fair
        fields = [
            'name', 'city', 'country', 'start_date', 'end_date', 'organizer', 'description'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ['start_date', 'end_date', 'description']:
                field.widget.attrs['class'] = 'form-control'


class BriefForm(forms.ModelForm):
    class Meta:
        model = Brief
        fields = [
            'stand_boyutu', 'stand_konumu', 'stand_tipi',
            'fiyat', 'para_birimi', 'gecerlilik_tarihi',
            'ozel_notlar', 'durum',
        ]
        widgets = {
            'gecerlilik_tarihi': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ozel_notlar': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ['gecerlilik_tarihi', 'ozel_notlar']:
                field.widget.attrs['class'] = 'form-control'


class ExcelImportForm(forms.Form):
    fair = forms.ModelChoiceField(queryset=Fair.objects.all(), required=False)
    excel_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fair'].widget.attrs['class'] = 'form-select'
        self.fields['excel_file'].widget.attrs['class'] = 'form-control'
