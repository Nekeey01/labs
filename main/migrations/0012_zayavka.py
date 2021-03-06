# Generated by Django 3.2 on 2022-05-13 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20220329_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zayavka',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_zayavka', models.DateField(verbose_name='День подачи заявки')),
                ('reserv_date', models.DateField(verbose_name='День')),
                ('reserv_time', models.CharField(blank=True, max_length=50, null=True, verbose_name='Время')),
                ('status', models.CharField(blank=True, max_length=50, null=True, verbose_name='Статус')),
                ('zayavka_cab', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.cabinet')),
                ('zayavka_user_iduser_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='zayavka_user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
    ]
