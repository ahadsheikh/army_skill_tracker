# Generated by Django 3.2.7 on 2021-12-30 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_company_subcriteria_subunit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soldier',
            name='previous_subunit',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
