# Generated by Django 4.1 on 2022-11-13 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0008_asset_business_unit_asset_idc_asset_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_model', models.CharField(blank=True, max_length=128, null=True, verbose_name='CPU型号')),
                ('cpu_count', models.PositiveSmallIntegerField(default=1, verbose_name='物理CPU个数')),
                ('cpu_core_count', models.PositiveSmallIntegerField(default=1, verbose_name='CPU核数')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cmdb.asset')),
            ],
            options={
                'verbose_name': 'CPU',
                'verbose_name_plural': 'CPU',
            },
        ),
    ]