# Generated by Django 3.2 on 2022-05-15 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_zayavka_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='zayavka',
            name='wish',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Пожелание к оборудованию'),
        ),
    ]