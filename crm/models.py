from django.db import models
from django.contrib.auth.models import User


class Fair(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    organizer = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-start_date', 'name']

    def __str__(self):
        return self.name


class Company(models.Model):
    STATUS_CHOICES = [
        ('katiliyor', 'Katılıyor'),
        ('katilmiyor', 'Katılmıyor'),
        ('ulasilamadi', 'Ulaşılamadı'),
        ('tekrar_ara', 'Tekrar Ara'),
        ('iptal', 'İptal'),
        ('teklif_ver', 'Teklif Ver'),
        ('sozlesme_hazirla', 'Sözleşme Hazırla'),
    ]

    ACTION_CHOICES = [
        ('ara', 'Ara'),
        ('mail_at', 'Mail At'),
        ('teklif_hazirla', 'Teklif Hazırla'),
        ('toplanti_yap', 'Toplantı Yap'),
        ('takip_et', 'Takip Et'),
    ]

    fair = models.ForeignKey(Fair, on_delete=models.SET_NULL, null=True, blank=True, related_name='companies')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='companies')

    company_id_code = models.CharField(max_length=50, blank=True)
    fair_id_code = models.CharField(max_length=50, blank=True)

    company_name = models.CharField(max_length=255)
    authorized_person = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)

    company_status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True)
    next_action = models.CharField(max_length=50, choices=ACTION_CHOICES, blank=True)
    last_contact = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['company_name']

    def __str__(self):
        return self.company_name


class Brief(models.Model):
    STATUS_CHOICES = [
        ('taslak', 'Taslak'),
        ('gonderildi', 'Gönderildi'),
        ('onaylandi', 'Onaylandı'),
        ('reddedildi', 'Reddedildi'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='briefs')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    stand_boyutu = models.CharField(max_length=100, blank=True, verbose_name='Stand Boyutu (m²)')
    stand_konumu = models.CharField(max_length=255, blank=True, verbose_name='Stand Konumu / Hol')
    stand_tipi = models.CharField(max_length=100, blank=True, verbose_name='Stand Tipi')

    fiyat = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Teklif Fiyatı')
    para_birimi = models.CharField(max_length=10, default='EUR', verbose_name='Para Birimi')
    gecerlilik_tarihi = models.DateField(null=True, blank=True, verbose_name='Geçerlilik Tarihi')

    ozel_notlar = models.TextField(blank=True, verbose_name='Özel Notlar')
    durum = models.CharField(max_length=20, choices=STATUS_CHOICES, default='taslak', verbose_name='Durum')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company.company_name} - Brief #{self.pk}"
