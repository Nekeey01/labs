from bootstrap_modal_forms.generic import BSModalUpdateView
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView

from main.forms import UpdateEquipmentForm
from main.models import Equipment
from main.utils import DataMixin

from datetime import datetime

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalLoginView, BSModalUpdateView
from bootstrap_modal_forms.utils import is_ajax
from django.contrib.auth import logout, login
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.views.generic import CreateView, ListView, UpdateView, FormView, TemplateView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from main.forms import *
from main.utils import *
