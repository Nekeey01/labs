from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse


## измененная таблица юзера, использующая дефолтный класс
class CustomUser(AbstractUser):
    avatar = models.ImageField('Аватар', upload_to='avatar/%Y/%m/%d/', default='avatar/default/kot.png')
    middle_name = models.CharField('Отчество', max_length=250, blank=True, null=True)
    def __str__(self):
        return self.username


## таблица интервалов времени
class TimeInterval(models.Model):
    time = models.CharField('Интервал', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Интервал времени'
        verbose_name_plural = "Интервалы времени"

    def __str__(self):
        return f"{self.time}"


## таблица ПО
class Equipment(models.Model):
    title = models.CharField('Название ПО', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Название ПО'
        verbose_name_plural = "Название ПО"

    def __str__(self):
        return f"{self.title}"


## таблица Кабинета
class Cabinet(models.Model):
    number = models.PositiveSmallIntegerField('Номер пк', unique=True)
    time_id = models.ManyToManyField(TimeInterval, related_name='time_id')
    equip_id = models.ManyToManyField(Equipment, related_name='equip_id')

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = "Кабинеты"

    def __str__(self):
        return f"{self.number}"

    def get_absolute_url(self):
        return reverse('reservation', kwargs={'cab_id': self.number})


class Reserved_Cabinet(models.Model):

    reserv_date = models.DateField('День')
    reserv_time = models.CharField('Время', max_length=50, null=True, blank=True)

    ## привязка пк
    cab = models.ForeignKey(Cabinet, on_delete=models.PROTECT)
    # reserv_time = models.ForeignKey(TimeInterval, on_delete=models.PROTECT)

    user_id = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='user_id')
    # reserv_time = models.ForeignKey(Cabinet, to_field="", on_delete=models.PROTECT, related_name='reserv_time_id', null=True, blank=True)


    class Meta:
        verbose_name = 'Зарезервированные кабинеты'
        verbose_name_plural = "Зарезервированные кабинеты"

    def __str__(self):
        return f"{self.cab.number}"




