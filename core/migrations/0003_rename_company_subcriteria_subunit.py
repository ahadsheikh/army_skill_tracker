# Generated by Django 3.2.7 on 2021-12-19 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_subcriteria_company'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcriteria',
            old_name='company',
            new_name='subunit',
        ),
    ]
