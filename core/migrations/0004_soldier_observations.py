# Generated by Django 3.2.7 on 2021-11-30 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20211130_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='soldier',
            name='observations',
            field=models.ManyToManyField(to='core.Observation'),
        ),
    ]
