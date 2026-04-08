import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brief',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stand_boyutu', models.CharField(blank=True, max_length=100, verbose_name='Stand Boyutu (m²)')),
                ('stand_konumu', models.CharField(blank=True, max_length=255, verbose_name='Stand Konumu / Hol')),
                ('stand_tipi', models.CharField(blank=True, max_length=100, verbose_name='Stand Tipi')),
                ('fiyat', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Teklif Fiyatı')),
                ('para_birimi', models.CharField(default='EUR', max_length=10, verbose_name='Para Birimi')),
                ('gecerlilik_tarihi', models.DateField(blank=True, null=True, verbose_name='Geçerlilik Tarihi')),
                ('ozel_notlar', models.TextField(blank=True, verbose_name='Özel Notlar')),
                ('durum', models.CharField(
                    choices=[
                        ('taslak', 'Taslak'),
                        ('gonderildi', 'Gönderildi'),
                        ('onaylandi', 'Onaylandı'),
                        ('reddedildi', 'Reddedildi'),
                    ],
                    default='taslak',
                    max_length=20,
                    verbose_name='Durum',
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='briefs', to='crm.company')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
