# Generated by Django 4.2.9 on 2024-01-19 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('city', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('hex_code', models.CharField(max_length=50, verbose_name='HexCode')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='car.basemodel')),
                ('plate', models.CharField(max_length=50, unique=True, verbose_name='Plate')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('car_value', models.PositiveBigIntegerField(default=0, verbose_name='Car Value')),
                ('mileage', models.CharField(choices=[('0-50/000', 'M0'), ('50/000-100/000', 'M50'), ('100/000-200/000', 'M100'), ('+200/000', 'M0200')], max_length=20, verbose_name='Mileage')),
                ('status', models.CharField(choices=[('accepted', 'Accepted'), ('pending', 'Pending'), ('rejected', 'Rejected')], default='pending', max_length=10, verbose_name='status')),
                ('is_out_of_service', models.BooleanField(default=False, verbose_name='Is_out_of_Service')),
                ('has_media', models.BooleanField(default=False, verbose_name='Has_Media')),
                ('has_complete_info', models.BooleanField(default=False, verbose_name='Has_Complete_Info')),
            ],
            bases=('car.basemodel',),
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='car.basemodel')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            bases=('car.basemodel',),
        ),
        migrations.CreateModel(
            name='CarOptions',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='car.basemodel')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
            ],
            bases=('car.basemodel',),
        ),
        migrations.CreateModel(
            name='CarYear',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='car.basemodel')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
            ],
            bases=('car.basemodel',),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='car.basemodel')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
            ],
            bases=('car.basemodel',),
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='car.basemodel')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            bases=('car.basemodel',),
        ),
        migrations.CreateModel(
            name='TechnicalSpecifications',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='car.basemodel')),
                ('body_style', models.CharField(choices=[('passenger_car', 'Passenger_Car'), ('suv', 'SUV'), ('convertible', 'Convertible'), ('coupe', 'Coupe'), ('van', 'Van'), ('pickup', 'Pickup')], max_length=15, verbose_name='Body Style')),
                ('gearbox_type', models.CharField(choices=[('manual', 'Manual'), ('automatic', 'Automatic')], max_length=9, verbose_name='Gearbox Type')),
                ('cylinder', models.PositiveSmallIntegerField(default=0, verbose_name='Cylinder')),
                ('capacity', models.PositiveIntegerField(default=0, verbose_name='Capacity')),
            ],
            bases=('car.basemodel',),
        ),
        migrations.CreateModel(
            name='RentalTerms',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='car.basemodel')),
                ('cancellation_policy', models.TextField(verbose_name='Rental Cancellation Terms')),
                ('min_days_to_rent', models.PositiveIntegerField(default=0, verbose_name='Min Days to Rent')),
                ('max_km_per_day', models.PositiveIntegerField(default=0, verbose_name='Max KM Per Day')),
                ('extra_km_price', models.PositiveIntegerField(default=0, verbose_name='Extra KM Price')),
                ('extra_hour_price', models.PositiveIntegerField(default=0, verbose_name='Extra Hour Price')),
                ('deliver_at_renters_place', models.BooleanField(default=False, verbose_name='Deliver_at_Renters_Place')),
                ('with_driver', models.BooleanField(default=False, verbose_name='With_Driver')),
                ('without_driver', models.BooleanField(default=False, verbose_name='Without_Driver')),
                ('price_each_day', models.PositiveBigIntegerField(default=False, verbose_name='Price Each Day')),
                ('car_object', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='car.car', verbose_name='Car')),
            ],
            bases=('car.basemodel',),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='car.basemodel')),
                ('text', models.TextField(verbose_name='text')),
                ('car_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Comment_car', to='car.car', verbose_name='Car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Comment_user', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            bases=('car.basemodel',),
        ),
        migrations.CreateModel(
            name='CarTemplate',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='car.basemodel')),
                ('Technical_specifications', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CarTemplate_TS', to='car.technicalspecifications', verbose_name='TechnicalSpecifications')),
                ('category', models.ManyToManyField(to='car.category', verbose_name='Category')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CarTemplate_model', to='car.carmodel', verbose_name='Model')),
            ],
            bases=('car.basemodel',),
        ),
        migrations.AddField(
            model_name='carmodel',
            name='manufacturers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car.manufacturer', verbose_name='Manufacturer'),
        ),
        migrations.CreateModel(
            name='CarImage',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='car.basemodel')),
                ('image', models.FileField(upload_to='images/', verbose_name='Image')),
                ('car_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car.car', verbose_name='Car')),
            ],
            bases=('car.basemodel',),
        ),
        migrations.AddField(
            model_name='car',
            name='car_option',
            field=models.ManyToManyField(to='car.caroptions', verbose_name='Car Options'),
        ),
        migrations.AddField(
            model_name='car',
            name='car_template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_car_template', to='car.cartemplate', verbose_name='Car Template'),
        ),
        migrations.AddField(
            model_name='car',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='car_city', to='city.city', verbose_name='City'),
        ),
        migrations.AddField(
            model_name='car',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='car_color', to='car.color', verbose_name='Car Color'),
        ),
        migrations.AddField(
            model_name='car',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_owner', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AddField(
            model_name='car',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='car_year', to='car.caryear', verbose_name='Car Year'),
        ),
    ]
