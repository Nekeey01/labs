# Generated by Django 3.2 on 2022-03-26 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_reserved_cabinet_reserv_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserved_cabinet',
            name='reserv_time',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Время'),
        ),
    ]
