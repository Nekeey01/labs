# Generated by Django 3.2 on 2022-05-13 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_zayavka'),
    ]

    operations = [
        migrations.RenameField(
            model_name='zayavka',
            old_name='zayavka_user_iduser_id',
            new_name='zayavka_user_id',
        ),
    ]
