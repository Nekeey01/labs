from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.urls import reverse


## измененная таблица юзера, использующая дефолтный класс
class CustomUser(AbstractUser):
    email = models.EmailField("Почта", unique=True, blank=False)
    first_name = models.CharField("Имя", max_length=250, blank=False)
    last_name = models.CharField("Фамилия", max_length=250, blank=False)
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


## таблица ПО
class Oborud(models.Model):
    title = models.CharField('Название оборудования', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Название оборудования'
        verbose_name_plural = "Название оборудования"

    def __str__(self):
        return f"{self.title}"


## таблица Кабинета
class Cabinet(models.Model):
    number = models.PositiveSmallIntegerField('Номер лаборатории', unique=True)
    time_id = models.ManyToManyField(TimeInterval, related_name='time_id')
    equip_id = models.ManyToManyField(Equipment, related_name='equip_id')
    oborud_id = models.ManyToManyField(Oborud, related_name='oborud_id')

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = "Кабинеты"

    def __str__(self):
        return f"{self.number}"

    def get_absolute_url(self):
        return reverse('reservation', kwargs={'cab_id': self.number})


## таблица оборудования
class Zayavka(models.Model):
    date_zayavka = models.DateField('День подачи заявки')

    reserv_date = models.DateField('День')
    reserv_time = models.CharField('Время', max_length=50, null=True, blank=True)

    ## привязка пк
    zayavka_cab = models.ForeignKey(Cabinet, on_delete=models.CASCADE)

    zayavka_user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='zayavka_user_id')

    status = models.CharField('Статус', max_length=50, null=True, blank=True)
    reason = models.CharField('Причина отказа', max_length=250, null=True, blank=True, default="")
    wish = models.TextField('Пожелание к оборудованию', max_length=250, null=True, blank=True, default="")

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.pk}"


class Reserved_Cabinet(models.Model):
    reserv_date = models.DateField('День')
    reserv_time = models.CharField('Время', max_length=50, null=True, blank=True)

    ## привязка пк
    cab = models.ForeignKey(Cabinet, on_delete=models.CASCADE)

    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_id')

    class Meta:
        verbose_name = 'Зарезервированные кабинеты'
        verbose_name_plural = "Зарезервированные кабинеты"

    def __str__(self):
        return f"{self.cab.number}"
