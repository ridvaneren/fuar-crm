from datetime import datetime
import pandas as pd
from .models import Company


COLUMN_MAP = {
    'FirmaID': 'company_id_code',
    'FuarID': 'fair_id_code',
    'Firma Adı': 'company_name',
    'Yetkili': 'authorized_person',
    'Telefon': 'phone',
    'Eposta': 'email',
    'Web': 'website',
    'Adres': 'address',
    'Firma Durumu': 'company_status',
    'Sonraki Eylem': 'next_action',
    'Son Temas': 'last_contact',
    'Notlar': 'notes',
}


def normalize_value(value):
    if pd.isna(value):
        return ''
    if isinstance(value, datetime):
        return value.date()
    return str(value).strip()


VALID_STATUS = {choice[0] for choice in Company.STATUS_CHOICES}
VALID_ACTION = {choice[0] for choice in Company.ACTION_CHOICES}


def import_companies_from_excel(file, fair=None, owner=None):
    df = pd.read_excel(file)
    created_count = 0
    skipped_count = 0

    for _, row in df.iterrows():
        data = {}
        for excel_col, model_field in COLUMN_MAP.items():
            if excel_col in df.columns:
                data[model_field] = normalize_value(row.get(excel_col))

        company_name = str(data.get('company_name', '')).strip()
        if not company_name:
            skipped_count += 1
            continue

        last_contact = data.get('last_contact') or None
        if isinstance(last_contact, str) and last_contact:
            try:
                last_contact = pd.to_datetime(last_contact).date()
            except Exception:
                last_contact = None

        company_status = data.get('company_status', '')
        if company_status and company_status not in VALID_STATUS:
            company_status = ''

        next_action = data.get('next_action', '')
        if next_action and next_action not in VALID_ACTION:
            next_action = ''

        Company.objects.create(
            fair=fair,
            owner=owner,
            company_id_code=data.get('company_id_code', ''),
            fair_id_code=data.get('fair_id_code', ''),
            company_name=company_name,
            authorized_person=data.get('authorized_person', ''),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            website=data.get('website', ''),
            address=data.get('address', ''),
            company_status=company_status,
            next_action=next_action,
            last_contact=last_contact,
            notes=data.get('notes', ''),
        )
        created_count += 1

    return created_count, skipped_count
