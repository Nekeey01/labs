# Generated by Django 3.2 on 2022-05-25 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20220526_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.EmailField(max_length=254, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.EmailField(max_length=254, verbose_name='Фамилия'),
        ),
    ]
