# Generated by Django 4.2.9 on 2024-01-27 16:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('car', '0002_car_is_available'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_rent_date', models.DateField(verbose_name='Start Rent Date')),
                ('min_days_to_rent', models.PositiveIntegerField(default=0, verbose_name='Min Days to Rent')),
                ('price_each_day', models.PositiveBigIntegerField(default=0, verbose_name='Price Each Day')),
                ('value_added', models.PositiveBigIntegerField(default=0, verbose_name='Value Added')),
                ('with_insurance', models.BooleanField(default=False, verbose_name='With_Insurance')),
                ('insurance_price', models.PositiveBigIntegerField(default=0, verbose_name='Insurance Price')),
                ('reserve_status', models.CharField(choices=[('accepted', 'Accepted'), ('pending', 'Pending'), ('rejected', 'Rejected')], default='pending', max_length=10, verbose_name='Reserver_Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated_at')),
                ('paid_date', models.DateTimeField(blank=True, null=True, verbose_name='Paid Date')),
                ('tracking_payment', models.CharField(blank=True, max_length=20, null=True, verbose_name='Tracking Payment')),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Bank Name')),
                ('payment_status', models.BooleanField(default=False, verbose_name='Payment_Status')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reserve_car', to='car.car', verbose_name='Car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserve_user', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
