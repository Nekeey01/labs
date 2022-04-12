from django.views.generic import CreateView
from django.urls import path, include

from . import views
from .views import *


urlpatterns = [
    path('', Index.as_view(), name='home'),

    path('login', LoginUser.as_view(), name='login'),

    path('logout', logout_user, name='logout'),
    path('reg', RegisterUser.as_view(), name='register'),

    path('show_pc', ListCabinet.as_view(), name='show_pc'),
    path('reservation/<slug:cab_id>', Reserv_Cab.as_view(), name='reservation'),

    path('show_pc_with_game', SomeAPI.as_view(), name='show_pc_with_game'),

    path('profile/<pk>', Profile.as_view(), name='profile'),
    path('create_cab', CreateCab.as_view(), name='create_cab'),
    path('create_time_interval', CreateTimeInterval.as_view(), name='create_time_interval'),
    path('load_teacher', LoadTeacher.as_view(), name='load_teacher'),
    path('create_equipment', CreateEquipment.as_view(), name='create_equipment'),
    path('create_teacher', CreateTeacher.as_view(), name='create_teacher'),


]
