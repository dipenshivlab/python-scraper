# Generated by Django 4.2.7 on 2023-12-05 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clutch_company', '0003_company_position'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='company_name',
            new_name='company',
        ),
    ]