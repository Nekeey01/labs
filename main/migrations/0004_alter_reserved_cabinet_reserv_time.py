# Generated by Django 3.2 on 2022-03-26 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20220326_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserved_cabinet',
            name='reserv_time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cab_time_id', to='main.cabinet'),
        ),
    ]
