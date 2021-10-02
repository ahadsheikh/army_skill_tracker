# Generated by Django 3.2.7 on 2021-10-02 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clerk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('type', models.CharField(choices=[('A', 'Admin'), ('C', 'Clerk'), ('S', 'Soldier')], default='C', max_length=1)),
                ('rank', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=20)),
                ('subunit', models.CharField(max_length=20)),
                ('starting_date', models.DateField(auto_now_add=True)),
                ('contact', models.CharField(max_length=50)),
                ('profile_pic', models.ImageField(blank=True, default='army.jpg', upload_to='profile_pics')),
            ],
        ),
    ]
