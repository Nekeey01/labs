# Generated by Django 3.2 on 2022-05-14 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_rename_zayavka_user_iduser_id_zayavka_zayavka_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='zayavka',
            name='reason',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Причина отказа'),
        ),
    ]
