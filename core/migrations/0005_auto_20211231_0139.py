# Generated by Django 3.2.7 on 2021-12-30 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_soldier_previous_subunit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soldier',
            name='last_promotion_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='soldier',
            name='previous_subunit',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]