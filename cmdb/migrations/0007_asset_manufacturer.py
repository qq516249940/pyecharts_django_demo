# Generated by Django 4.1 on 2022-11-12 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0006_contract_idc_manufacturer_tag_businessunit'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cmdb.manufacturer', verbose_name='制造商'),
        ),
    ]
