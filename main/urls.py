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

    ########   ADMIN    ############
    path('update_equipment/<pk>', UpdateEquipment.as_view(), name='update_equipment'),
    path('list_equipment', ListEquipment.as_view(), name='list_equipment'),
    path('equips', equips, name='equips'),
    path('create_equipment', CreateEquipment.as_view(), name='create_equipment'),

    #__time__#
    path('update_time/<pk>', UpdateTime.as_view(), name='update_time'),
    path('list_times', ListTime.as_view(), name='list_times'),
    path('times', times, name='times'),
    path('create_time_interval', CreateTimeInterval.as_view(), name='create_time_interval'),

    #__Cabinet__#
    path('update_cab/<pk>', UpdateCabs.as_view(), name='update_cab'),
    path('list_cab', ListCabs.as_view(), name='list_cab'),
    path('cab', cab, name='cab'),
    path('create_cab', CreateCab.as_view(), name='create_cab'),

    #__Teacher__#
    path('update_teacher/<pk>', UpdateTeacher.as_view(), name='update_teacher'),
    path('list_teacher', ListTeacher.as_view(), name='list_teacher'),
    path('teacher', teacher, name='teacher'),
    path('create_teacher', CreateTeacher.as_view(), name='create_teacher'),
    path('load_teacher', LoadTeacher.as_view(), name='load_teacher'),

    # __Oborudovanie__#
    path('update_oborud/<pk>', UpdateOborud.as_view(), name='update_oborud'),
    path('list_oborud', ListOborud.as_view(), name='list_oborud'),
    path('oborud', oborud, name='oborud'),
    path('create_oborud', CreateOborud.as_view(), name='create_oborud'),


    #__заявка__#
    path('list_users_zayavka/<pk>', ListUsersZayavka.as_view(), name='list_users_zayavka'),
    path('reserved_cab', ListResCab.as_view(), name='reserved_cab'),

    path('list_zayvka_from_ucheb', ShowZayvkaFromUcheb.as_view(), name='list_zayvka_from_ucheb'),
    path('journal_zayavok', ShowJournal.as_view(), name='journal_zayavok'),
    path('update_zayvka_from_ucheb/<pk>', UpdateZayvkaFromUcheb.as_view(), name='update_zayvka_from_ucheb'),

    path('list_zayvka_from_inf', ShowZayvkaFromInf.as_view(), name='list_zayvka_from_inf'),
    path('update_zayvka_from_inf/<pk>', UpdateZayvkaFromInf.as_view(), name='update_zayvka_from_inf'),


]
