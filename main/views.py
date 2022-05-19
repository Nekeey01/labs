from datetime import datetime

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalLoginView, BSModalUpdateView
from django.contrib.auth import logout, login
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.views.generic import CreateView, ListView, UpdateView, FormView, TemplateView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import *
from .utils import *


## вьюха главной странички


class Index(DataMixin, ListView):
    model = Cabinet
    template_name = "main/index.html"
    context_object_name = "po"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Главная!", count_lab=Cabinet.objects.count(),
                                      res_lab=Reserved_Cabinet.objects.count())
        return dict(list(context.items()) + list(c_def.items()))

    ## получает список тасков, начиная с последнего созданного
    def get_queryset(self):
        return Equipment.objects.order_by('-id')


## регистрация пользователя
class RegisterUser(DataMixin, BSModalCreateView):
    form_class = CreateUserForm
    template_name = 'main/create_user.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Регистрация!")
        return dict(list(context.items()) + list(c_def.items()))

    ## функция, вызывающаяся при валидности формы
    def form_valid(self, form):
        if not self.request.is_ajax():
            user = form.save()  ## сохранение формы
            login(self.request, user)  ## авто-логин пользователя при регистрации
        return redirect('home')


## логин пользователя
class LoginUser(DataMixin, BSModalLoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Авторизируйся!")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


## функция выхода пользователя
def logout_user(request):
    logout(request)
    return redirect('home')


class ListCabinet(DataMixin, ListView):
    model = Cabinet
    template_name = "main/show_pc.html"
    context_object_name = "cab"
    queryset = Cabinet.objects.filter().order_by("number")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Выбери кабинет", time_interval=TimeInterval.objects.all())
        return dict(list(context.items()) + list(c_def.items()))


class SomeAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main/list_pc.html'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('gg')  ## запрос строки
        d_s = self.request.GET.get('date_start')  ## дата, выбранная для фильтрации
        t_s = self.request.GET.get('time_choice')  ## время, выбранная для фильтрации
        # d_e = self.request.GET.get('date_end')
        check_date = False
        check_time = False
        free_cab = Cabinet.objects.all().order_by("number")  ## ищем свободные кабинеты среди всех

        if d_s != '':
            date_start = make_aware(datetime.strptime(d_s, '%d.%m.%Y')).date()  ## вытаскиваем день
            check_date = True
        if t_s != '':
            time_start = t_s  ## вытаскиваем время
            check_time = True
        if query != '':
            free_cab = return_cab_with_equ(query)  ## ищем кабинеты по ПО
            print("free_cab - ", free_cab)
            # free_cab = Cabinet.objects.filter(Q(equip_id__title__icontains=query)).order_by("number")  ## ищем кабинеты по ПО

        print("check_date - ", d_s)
        print("check_time - ", t_s)
        ## Если дата есть в фильтрации, то ищем среди пк выше те, у которых даты совпадают и убираем их
        if check_date or check_time:
            ## поиск в зарезервированных пк
            request.session['reserv_times'] = d_s  ## устанавливаем дату в сессию
            request.session['reserv_time_inteval'] = time_start  ## устанавливаем время в сессию
            if check_date and check_time:
                o = Reserved_Cabinet.objects.filter(Q(reserv_date=date_start) & Q(reserv_time=time_start)).distinct()

                if time_start == "Свободные кабинеты":
                    o = Reserved_Cabinet.objects.filter(Q(reserv_date=date_start)).distinct()
                    free_pc_and_o = Cabinet.objects.filter(
                        Q(number__in=o.values_list('cab__number', flat=True).order_by(
                            "cab__number")))  ## ищем во всех пк те, которые подходят в резервированных

                elif time_start == "Любое время":
                    free_pc_and_o = Cabinet.objects.none()
                    print("Любое время - ", free_pc_and_o)
                else:
                    free_pc_and_o = Cabinet.objects.filter(
                        ~Q(time_id__time=time_start) | Q(number__in=o.values_list('cab__number', flat=True).order_by(
                            "cab__number")))  ## ищем во всех пк те, которые подходят в резервированных

                print("O - ", o)

                print("free_pc_and_o - ", free_pc_and_o)
                g = free_cab.difference(free_pc_and_o)  ## убираем лишнее

            elif time_start == "Любое время":
                g = free_cab

            elif time_start == "Свободные кабинеты":
                request.session['reserv_time_inteval'] = False
                o = Reserved_Cabinet.objects.all().distinct()

                free_pc_and_o = Cabinet.objects.filter(
                    Q(number__in=o.values_list('cab__number', flat=True).order_by(
                        "cab__number")))  ## ищем во всех пк те, которые подходят в резервированных
                g = free_cab.difference(free_pc_and_o).order_by("number")  ## убираем лишнее

            elif check_time:
                o = Cabinet.objects.filter(Q(time_id__time=time_start)).distinct()
                print("O", o)
                # request.session['reserv_times'] = d_s  ## устанавливаем дату в сессию
                # request.session['reserv_time_inteval'] = time_start  ## устанавливаем время в сессию
                free_pc_and_o = o
                g = o

            print("G - ", g)

            return Response({'cab': g})

        print("!!!! - ", free_cab)
        request.session['reserv_times'] = False
        request.session['reserv_time_inteval'] = False
        return Response({'cab': free_cab})

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax and self.request.POST.get('click'):

            if self.request.user.is_authenticated:
                data = {"status": 1, "url": 'home'}
                return JsonResponse(data)
            else:
                data = {"status": 0, "url": 'about'}
                return JsonResponse(data)


def return_cab_with_equ(query):
    query_list = query.split(';')
    print("query_list - ", query_list)
    q = Q()
    for st in query_list:
        if st.strip() == '':
            continue
        q |= Q(equip_id__title__icontains=st.strip())
    return Cabinet.objects.filter(q)


## резервация пк обычным пользователем
class Reserv_Cab(DataMixin, CreateView):
    form_class = Reserv_Cab_Form
    template_name = 'main/reservation.html'
    success_url = reverse_lazy('show_pc')
    gg = 0
    user_id = 0
    intervals = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Создать заявку",
                                      date=self.request.session['reserv_times'] if self.request.session.get(
                                          'reserv_times', False) else '',
                                      res_time=self.request.session['reserv_time_inteval'] if self.request.session.get(
                                          'reserv_time_inteval', False) else '',
                                      list_times=Cabinet.objects.filter(number=self.kwargs['cab_id']).values_list(
                                          "time_id__time", flat=True).order_by('time_id__time'))
        return dict(list(context.items()) + list(c_def.items()))

    def get_form_kwargs(self):
        kwargs = super(Reserv_Cab, self).get_form_kwargs()
        # print(self.kwargs['cab_id'])
        kwargs['cab_id'] = self.kwargs['cab_id']
        return kwargs

    def post(self, request, *args, **kwargs):
        self.intervals = request.POST.getlist('intervals')
        print("fruits - ", self.intervals)
        form = self.get_form(self.form_class)
        if form.is_valid():
            print("ФОРМА БАЛДЕЖ")
            self.gg = Cabinet.objects.get(number=int(self.kwargs['cab_id']))

            self.user_id = request.user  ## принимаем айди юзера из реквеста

            return self.form_valid(form)  ## возвращается дефолтный метод
        else:
            print("ФОРМА АШИБКА")
            return super(Reserv_Cab, self).post(self, request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.cab = self.gg  ## "ссылка" на пк
        form.instance.user_id = self.user_id

        # TODO: добавить на каждой итерации, забронирован ли данный кабинет на это время, и если да - выводить на какое время он забронирован, но остальные создать
        for g in self.intervals:

            if g == None:
                continue
            if Reserved_Cabinet.objects.filter(
                    Q(cab=self.gg) & Q(reserv_date=form.cleaned_data['reserv_date']) & Q(reserv_time=g)).exists():
                print("НИЗЯ ТАК ДЕЛАЦ")
                continue

            po = ""

            # TOD: Изменить
            # res_cab = Reserved_Cabinet(reserv_date=form.cleaned_data['reserv_date'], reserv_time=g, cab=self.gg, user_id=self.user_id)
            # res_cab.save()
            res_cab = Zayavka(date_zayavka=datetime.now().strftime('%Y-%m-%d'),
                              reserv_date=form.cleaned_data['reserv_date'], reserv_time=g, zayavka_cab=self.gg,
                              zayavka_user_id=self.user_id, status="В ожидании", wish=form.cleaned_data['wish'])
            res_cab.save()
            for i in self.gg.equip_id.all():
                po += f"{i}, "
            print(po)
            email = EmailMessage(f"Резервация лаборатории № {self.gg}",
                                 f"Здравствуйте {self.user_id.first_name} {self.user_id.last_name}\nВы в {datetime.now().strftime('%H:%M')} зарезервировали лабораторию №{self.gg}\nВся информация по резервации:\nДата - {form.cleaned_data['reserv_date']}\nВремя - {g}\nНомер кабинета - {self.gg}\nПО, имеющееся в кабинете - {po}",
                                 to=[self.user_id.email])
            # email.send()

        # return super(Reserv_Cab, self).form_valid(form)
        return HttpResponseRedirect(self.success_url)
        # return reverse_lazy("home")


## Вьюха профиля
class Profile(DataMixin, UpdateView):
    model = CustomUser
    template_name = 'main/profile.html'
    fields = ['avatar']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Твой профиль", user=self.request.user,
                                      reserv_cab=Reserved_Cabinet.objects.filter(Q(user_id=self.request.user)).order_by(
                                          "cab__number"))
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('profile', args=[self.kwargs['pk']])  ## передаем "слагом" пк юзера

    def post(self, request, *args, **kwargs):
        ## если данные отправлены и имя кнопки == btn_videocard, то определяем эту форму как дефолтную
        if request.method == 'POST':
            print("request.POST - ", request.POST)

            for key in request.POST.keys():
                print("KEY - ", key)
                if key.startswith('btn_'):
                    btn_pk = key[4:]
                    print("btn_pk - ", btn_pk)

                    record = Reserved_Cabinet.objects.get(id=btn_pk)
                    print("record - ", record)
                    record.delete()
                    print("record.delete()")

                    # form = self.get_form(self.form_class)
                    # if form.is_valid():
                    #     return self.form_valid(form)
                    # else:
                    # return reverse_lazy('profile', args=[self.kwargs['pk']])
                    return super(Profile, self).post(self, request, *args, **kwargs)

                    # return HttpResponse("ашибка!!!")

            form = self.get_form(self.form_class)
            if form.is_valid():
                return super(Profile, self).post(self, request, *args, **kwargs)
            else:
                return HttpResponse("ашибка!!!")


## Создание ПО
class CreateEquipment(DataMixin, CreateView):
    form_class = CreateEquipmentForm
    template_name = 'main/create_equipment.html'
    success_url = reverse_lazy('create_equipment')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Добавить ПО")
        return dict(list(context.items()) + list(c_def.items()))


## Создание кабинета
class CreateCab(DataMixin, CreateView):
    form_class = CreateCabForm
    template_name = 'main/create_cab.html'
    success_url = reverse_lazy('create_cab')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Добавить лабораторию")
        return dict(list(context.items()) + list(c_def.items()))


## Создание интервалов времени
class CreateTimeInterval(DataMixin, CreateView):
    form_class = CreateTimeIntervalForm
    template_name = 'main/create_time_inteval.html'
    success_url = reverse_lazy('create_time_interval')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Добавить интервал времени")
        return dict(list(context.items()) + list(c_def.items()))


## загрузка учителей
class LoadTeacher(DataMixin, FormView):
    form_class = LoadTeacherForm
    template_name = 'main/load_teacher.html'
    success_url = reverse_lazy('load_teacher')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Загрузить преподавателей")
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file_field'])

            return self.form_valid(form)
        else:
            return super(LoadTeacher, self).post(self, request, *args, **kwargs)


def handle_uploaded_file(f):
    schet = 0
    for line in f:
        try:
            schet += 1
            st = line.decode('cp1251').split(';')
            print(st)

            last_name = st[0].strip()
            first_name = st[1].strip()
            middle_name = st[2].strip()
            email = st[3].strip()
            password = st[4].strip()

            print(last_name)
            print(first_name)
            print(middle_name)
            print(email)
            print(password)

            user = CustomUser.objects.create_user(email, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.middle_name = middle_name
            user.save()

            email = EmailMessage(f"Регистрация на платформе бронирования лабораторий",
                                 f"Здравствуйте {first_name} {last_name}\nВаш логин для входа на сайт - {email} \nВаш пароль - {password}",
                                 to=[email])
            # email.send()
            my_group = Group.objects.get(name='Teacher')
            my_group.user_set.add(user)

        except:
            print("АШИБКА В СТРОКЕ ", schet)


## Создание кабинета
class CreateTeacher(DataMixin, CreateView):
    form_class = CreateTeacherForm
    template_name = 'main/create_teacher.html'
    success_url = reverse_lazy('create_teacher')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Добавить преподавателя")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        middle_name = form.cleaned_data['middle_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = CustomUser.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.middle_name = middle_name
        user.save()
        email = EmailMessage(f"Регистрация на платформе бронирования лабораторий",
                             f"Здравствуйте {first_name} {last_name}\nВаш логин для входа на сайт - {email} \nВаш пароль - {password}",
                             to=[email])
        # email.send()

        my_group = Group.objects.get(name='Teacher')
        my_group.user_set.add(user)

        return HttpResponseRedirect(self.success_url)


############# ЗАЯВКИ #####################
class ListUsersZayavka(DataMixin, ListView):
    model = Zayavka
    template_name = "main/Teacher/list_users_zayavka.html"
    context_object_name = "Zayavka_in_time"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Список моих заявок", Zayavka_complete=Zayavka.objects.filter(
            Q(zayavka_user_id=self.kwargs['pk']) & (Q(status="Отклонена") | Q(status="Одобрено"))).order_by(
            '-id'))
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Zayavka.objects.filter(
            Q(zayavka_user_id=self.kwargs['pk']) & (
                    Q(status="Одобрено инф отделом") | Q(status="В ожидании"))).order_by(
            '-id')

    def get(self, request, *args, **kwargs):
        for key in request.GET.keys():
            if key.startswith('btn_'):
                btn_pk = key[4:]
                record = Zayavka.objects.get(id=btn_pk)
                record.status = "Отклонена пользователем"
                record.save()

        return super(ListUsersZayavka, self).get(request, *args, **kwargs)


class ShowZayvkaFromUcheb(DataMixin, ListView):
    model = Zayavka
    template_name = "main/ucheb/list_zayvka_from_ucheb.html"
    context_object_name = "Zayavka"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Список заявок")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Zayavka.objects.filter(Q(status="Одобрено инф отделом")).order_by('-id')

    def get(self, request, *args, **kwargs):
        for key in request.GET.keys():
            if key.startswith('btn_'):
                btn_pk = key[4:]
                record = Zayavka.objects.get(id=btn_pk)
                record.status = "Одобрено"
                record.save()

                res_cab = Reserved_Cabinet(reserv_date=record.reserv_date, reserv_time=record.reserv_time,
                                           cab=record.zayavka_cab,
                                           user_id=record.zayavka_user_id)
                res_cab.save()

        return super(ShowZayvkaFromUcheb, self).get(request, *args, **kwargs)


class ShowJournal(DataMixin, ListView):
    model = Zayavka
    template_name = "main/ucheb/journal.html"
    context_object_name = "Journal"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Журнал всех заявок")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Zayavka.objects.all().order_by('-id')

    def get(self, request, *args, **kwargs):
        for key in request.GET.keys():
            if key.startswith('btn_'):
                btn_pk = key[4:]
                record = Zayavka.objects.get(id=btn_pk)
                record.delete()

        return super(ShowJournal, self).get(request, *args, **kwargs)


## Создание кабинета
class UpdateZayvkaFromUcheb(DataMixin, BSModalUpdateView):
    model = Zayavka
    form_class = UpdateZayvkaForm
    template_name = 'main/ucheb/update_zayvka_from_ucheb.html'
    success_url = reverse_lazy('list_zayvka_from_ucheb')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Укажите причину отклонения заявки")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.status = "Отклонена"
        form.save()
        response = super().form_valid(form)
        return response


class ShowZayvkaFromInf(DataMixin, ListView):
    model = Zayavka
    template_name = "main/inf/list_zayvka_from_inf.html"
    context_object_name = "Zayavka"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Список заявок как инф")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Zayavka.objects.filter(Q(status="В ожидании")).order_by('-id')

    def get(self, request, *args, **kwargs):
        for key in request.GET.keys():
            if key.startswith('btn_'):
                btn_pk = key[4:]
                record = Zayavka.objects.get(id=btn_pk)
                record.status = "Одобрено инф отделом"
                record.save()

        return super(ShowZayvkaFromInf, self).get(request, *args, **kwargs)


## Создание кабинета
class UpdateZayvkaFromInf(DataMixin, BSModalUpdateView):
    model = Zayavka
    form_class = UpdateZayvkaForm
    template_name = 'main/inf/update_zayvka_from_inf.html'
    success_url = reverse_lazy('list_zayvka_from_inf')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Укажите причину отклонения заявки")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.status = "Отклонена"
        form.save()
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('list_zayvka_from_inf')


## Аналитика
class Analitics(DataMixin, TemplateView):
    template_name = 'main/analitics/analitics.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Аналитика",
                                      qs=Reserved_Cabinet.objects.all().values_list('reserv_date', flat=True).distinct().order_by('reserv_date'),
                                      qs2=Reserved_Cabinet.objects.values('reserv_date').annotate(count_reslabs=Count('reserv_date')).order_by('reserv_date'),

                                      qss=Zayavka.objects.all().values_list('status', flat=True).distinct().order_by("status"),
                                      qss2=Zayavka.objects.values('status').annotate(count_zayavok=Count('status')).order_by("status"))
        return dict(list(context.items()) + list(c_def.items()))
