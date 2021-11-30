# Generated by Django 3.2.7 on 2021-11-30 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Criteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mark', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='SubCriteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mark', models.PositiveIntegerField(default=0)),
                ('criteria_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.criteria')),
            ],
        ),
    ]
