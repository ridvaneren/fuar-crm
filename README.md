# Fuar CRM v1

Bu proje, fuar katılımcı listelerini Excel'den içe alıp web tabanlı CRM olarak yönetmek için hazırlanmış bir Django başlangıç projesidir.

## Özellikler
- Kullanıcı girişi
- Dashboard
- Firma listeleme, ekleme, düzenleme, silme
- Fuar listeleme, ekleme, düzenleme, silme
- Excel içe aktarma
- Excel dışa aktarma
- Arama ve filtreleme

## Kurulum

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Giriş adresi
- http://127.0.0.1:8000/accounts/login/

## Notlar
- Başlangıç veritabanı SQLite'tır.
- Yayına çıkarken PostgreSQL'e geçmek daha doğru olur.
- Import ekranı beklenen sütun adlarına göre çalışır.
- Bu sürümde duplicate kontrolü henüz yoktur.
