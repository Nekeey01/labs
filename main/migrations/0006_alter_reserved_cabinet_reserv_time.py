# Generated by Django 3.2 on 2022-03-26 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_reserved_cabinet_reserv_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserved_cabinet',
            name='reserv_time',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reserv_time_id', to='main.cabinet'),
        ),
    ]
