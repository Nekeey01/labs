import re

from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm

from .models import *


## форма создания юзера
class CreateUserForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', "username", "password1", "password2", "email")


## форма логина
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Логин', 'type': 'text', "autocomplete": "username"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Пароль', 'type': 'password'}))


class Reserv_Cab_Form(ModelForm):

    def __init__(self, cab_id=None, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(Reserv_Cab_Form, self).__init__(*args, **kwargs)
        print("BOOOBA - ", Cabinet.objects.filter(number=cab_id).values_list("time_id__time",
                                                                             flat=True))
        self.cab_id = cab_id

    class Meta:
        # model = Reserved_Cabinet
        model = Zayavka
        fields = ["reserv_date", 'wish']
        widgets = {
            "reserv_date": forms.DateInput(attrs={'class': 'form-control datepicker mr-2', 'id': 'datepicker', }),
        }


class LoadTeacherForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput())


class ClassStyleForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(ClassStyleForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UpdateZayvkaForm(ClassStyleForm):
    class Meta:
        model = Zayavka
        fields = ['reason']


class UpdateEquipmentForm(ClassStyleForm):
    class Meta:
        model = Equipment
        fields = ['title']


class UpdateOborudForm(ClassStyleForm):
    class Meta:
        model = Oborud
        fields = ['title']


class UpdateIntervalForm(ClassStyleForm):
    class Meta:
        model = TimeInterval
        fields = ['time']

    def clean_time(self):
        number = self.cleaned_data['time']
        tpl = "^([0-1]?[0-9]|2[0-3]):[0-5][0-9]-([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"
        print(number)
        if re.match(tpl, number) is not None:
            return number
        else:
            raise forms.ValidationError("Формат времени обязан быть XX:XX-XX:XX")


class UpdateCabForm(ClassStyleForm):
    def __init__(self, *args, **kwargs):
        super(UpdateCabForm, self).__init__(*args, **kwargs)
        self.fields['oborud_id'].label = 'Выберите оборудование'
        self.fields['time_id'].label = "Выберите интервалы времени"
        self.fields['equip_id'].label = "Выберите ПО"

    class Meta:
        model = Cabinet
        fields = ["number", "time_id", "equip_id", "oborud_id"]


class UpdateTeacherForm(BSModalModelForm):
    class Meta:
        model = CustomUser
        fields = ["last_name", "first_name", "middle_name", "email", "password", "groups"]


class Media:
    css = {
        'all': ('/admin/css/widgets.css',),
    }
    js = ('/admin/jsi18n/',)
