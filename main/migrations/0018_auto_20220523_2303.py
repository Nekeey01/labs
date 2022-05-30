# Generated by Django 3.2 on 2022-05-23 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20220518_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Oborud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Название оборудования')),
            ],
            options={
                'verbose_name': 'Название оборудования',
                'verbose_name_plural': 'Название оборудования',
            },
        ),
        migrations.AddField(
            model_name='cabinet',
            name='oborud_id',
            field=models.ManyToManyField(related_name='oborud_id', to='main.Oborud'),
        ),
    ]