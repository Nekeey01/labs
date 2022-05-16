from django.views.generic import CreateView
from django.urls import path, include

from . import views
from .views import *


urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('analitic', Analitics.as_view(), name='analitic'),

    path('login', LoginUser.as_view(), name='login'),

    path('logout', logout_user, name='logout'),
    path('reg', RegisterUser.as_view(), name='register'),

    path('show_pc', ListCabinet.as_view(), name='show_pc'),
    path('reservation/<slug:cab_id>', Reserv_Cab.as_view(), name='reservation'), # создание заявки

    path('show_pc_with_game', SomeAPI.as_view(), name='show_pc_with_game'),

    path('profile/<pk>', Profile.as_view(), name='profile'),
    path('create_cab', CreateCab.as_view(), name='create_cab'),
    path('create_time_interval', CreateTimeInterval.as_view(), name='create_time_interval'),
    path('load_teacher', LoadTeacher.as_view(), name='load_teacher'),
    path('create_equipment', CreateEquipment.as_view(), name='create_equipment'),
    path('create_teacher', CreateTeacher.as_view(), name='create_teacher'),

    #__заявка__#
    path('list_users_zayavka/<pk>', ListUsersZayavka.as_view(), name='list_users_zayavka'),

    path('list_zayvka_from_ucheb', ShowZayvkaFromUcheb.as_view(), name='list_zayvka_from_ucheb'),
    path('journal_zayavok', ShowJournal.as_view(), name='journal_zayavok'),
    path('update_zayvka_from_ucheb/<pk>', UpdateZayvkaFromUcheb.as_view(), name='update_zayvka_from_ucheb'),

    path('list_zayvka_from_inf', ShowZayvkaFromInf.as_view(), name='list_zayvka_from_inf'),
    path('update_zayvka_from_inf/<pk>', UpdateZayvkaFromInf.as_view(), name='update_zayvka_from_inf'),


]
