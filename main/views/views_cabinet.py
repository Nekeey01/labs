

from .imports import *


# ## Создание кабинета
# class CreateCab(DataMixin, CreateView):
#     form_class = CreateCabForm
#     template_name = 'main/admin/Cabinet/create_cab.html'
#     success_url = reverse_lazy('create_cab')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_content(title="Добавить лабораторию")
#         return dict(list(context.items()) + list(c_def.items()))


## Создание интервалов времени
class CreateCab(BSModalCreateView):
    form_class = UpdateCabForm
    template_name = 'main/admin/Cabinet/create_cab.html'
    success_url = reverse_lazy('list_cab')

def cab(request):
    data = dict()
    if request.method == 'GET':
        books = Cabinet.objects.all()
        # asyncSettings.dataKey = 'table'
        data['tables'] = render_to_string(
            'main/admin/Cabinet/_cab_table.html',
            {'Cab': books},
            request=request
        )
        return JsonResponse(data)


## список_заявок
class ListCabs(DataMixin, ListView):
    model = Cabinet
    template_name = "main/admin/Cabinet/list_cab.html"
    context_object_name = "Cab"
    queryset = Cabinet.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Время")
        return dict(list(context.items()) + list(c_def.items()))

    def get(self, request, *args, **kwargs):
        for key in request.GET.keys():
            if key.startswith('btn_'):
                btn_pk = key[4:]
                record = Cabinet.objects.get(id=btn_pk)
                record.delete()

        return super(ListCabs, self).get(request, *args, **kwargs)


## Обновление кабинета
class UpdateCabs(DataMixin, BSModalUpdateView):
    model = Cabinet
    form_class = UpdateCabForm
    template_name = 'main/admin/Cabinet/update_cab.html'
    success_message = 'DDDDDDDDDDD.'
    success_url = reverse_lazy('list_cab')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Укажите причину отклонения заявки")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            form.save()
        return super().form_valid(form)








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
                g = free_cab.difference(free_pc_and_o).order_by("number")  ## убираем лишнее

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
                o = Cabinet.objects.filter(Q(time_id__time=time_start)).distinct().order_by("number")
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
        q |= Q(oborud_id__title__icontains=st.strip())
    return Cabinet.objects.filter(q).distinct()


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

            self.user_id = request.user  ## принимаем ID юзера из реквеста

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