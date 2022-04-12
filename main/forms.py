from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q

from .models import *
from django.forms import ModelForm, TextInput, Textarea, ChoiceField, MultipleChoiceField, CheckboxSelectMultiple, \
    Select, SelectMultiple
from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm


## форма создания юзера
class CreateUserForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        # fields = ("name", "surname", "number", "email")
        fields = ('first_name', 'last_name', "username", "password1", "password2", "email")


## форма логина
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Логин', 'type': 'text', "autocomplete": "username"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Пароль', 'type': 'password'}))


## форма создания Кабинета
class CreateCabForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateCabForm, self).__init__(*args, **kwargs)
        self.fields['number'].widget.attrs['class'] = 'form-control'
        self.fields['time_id'].label = "Выберите интервалы времени"
        self.fields['equip_id'].label = "Выберите ПО"


    class Meta:
        model = Cabinet
        fields = ["number", "time_id", "equip_id"]

    # # валидатор
    # def clean_number(self):
    #     number = self.cleaned_data['number']
    #     if Cabinet.objects.filter(number=number).exists():
    #         raise forms.ValidationError("Номер этого сабинета уже существует")
    #     return number



class Reserv_Cab_Form(ModelForm):
    # reserv_time = forms.ModelChoiceField(queryset=None, to_field_name="number", empty_label="booba", required=False)
    # reserv_time = forms.ChoiceField(choices=(('1', '2'),))
    def __init__(self, cab_id=None, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(Reserv_Cab_Form, self).__init__(*args, **kwargs)
        # print("cab_id - ", cab_id)
        print("BOOOBA - ", Cabinet.objects.filter(number=cab_id).values_list("time_id__time", flat=True)) #<QuerySet ['10:00-12:00', '12:00-14:00', '8:00-10:00']>
        self.cab_id = cab_id
        # self.fields['reserv_time'].choices = [(i, str(i)) for i in Cabinet.objects.filter(number=cab_id).values_list("time_id__time", flat=True)]

    class Meta:
        model = Reserved_Cabinet
        fields = ["reserv_date"]
        widgets = {
            "reserv_date": forms.DateInput(attrs={'class': 'form-control datepicker mr-2', 'id': 'datepicker', }),
            ## выпадающий список
            # "start_time": forms.TimeInput(attrs={'class': 'form-control ml-1', 'type': "time", 'id': 'rest_example_1'}),
            # "reserv_time": forms.Select(attrs={'class': 'form-control mr-2', }),

        }
    # валидатор

    # def clean(self):
    #     cleaned_data = super().clean()
    #     print("NUMBER - ", self.cab_id)
    #     number = self.cab_id
    #     reserv_date = cleaned_data.get('reserv_date')
    #     reserv_time = cleaned_data.get('reserv_time')
    #     if Reserved_Cabinet.objects.filter(Q(cab__number=number) & Q(reserv_date=reserv_date) & Q(reserv_time=reserv_time)).exists():
    #         msg = "Этот кабинет на эту дату и время уже забронирован."
    #         self.add_error('reserv_time', msg)


import re

## форма создания интервала времени
class CreateTimeIntervalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateTimeIntervalForm, self).__init__(*args, **kwargs)
        self.fields['time'].widget.attrs['class'] = 'form-control'


    class Meta:
        model = TimeInterval
        fields = ["time"]

    def clean_time(self):
        number = self.cleaned_data['time']
        tpl = "^([0-1]?[0-9]|2[0-3]):[0-5][0-9]-([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"
        print(number)
        if re.match(tpl, number) is not None:
            return number
        else:
        # if Cabinet.objects.filter(number=number).exists():
            raise forms.ValidationError("Формат времени обязан быть XX:XX-XX:XX")
        # return number


## форма создания ПК
class CreateEquipmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateEquipmentForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Equipment
        fields = ["title"]


class LoadTeacherForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))


class CreateTeacherForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateTeacherForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].label = 'Фамилия'

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].label = 'Имя'
        self.fields['middle_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ["last_name", "first_name", "middle_name", "email", "password"]