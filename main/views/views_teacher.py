from .imports import *


## загрузка учителей
class LoadTeacher(DataMixin, FormView):
    form_class = LoadTeacherForm
    template_name = 'main/admin/Teacher/load_teacher.html'
    success_url = reverse_lazy('list_teacher')

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
            print("ОШИБКА В СТРОКЕ ", schet)


## Создание пользователя
class CreateTeacher(BSModalCreateView):
    form_class = UpdateTeacherForm
    template_name = 'main/admin/Teacher/create_teacher.html'
    success_url = reverse_lazy('list_teacher')

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            middle_name = form.cleaned_data['middle_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            groups = form.cleaned_data['groups']

            user = CustomUser.objects.create_user(email, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.middle_name = middle_name
            user.save()
            email = EmailMessage(f"Регистрация на платформе бронирования лабораторий",
                                 f"Здравствуйте {first_name} {last_name}\nВаш логин для входа на сайт - {email} \nВаш пароль - {password}",
                                 to=[email])
            # email.send()

            for i in groups:
                print(i)
                my_group = Group.objects.get(name=i)
                my_group.user_set.add(user)

        return HttpResponseRedirect(self.success_url)


def teacher(request):
    data = dict()
    if request.method == 'GET':
        books = CustomUser.objects.all()
        # asyncSettings.dataKey = 'table'
        data['tables'] = render_to_string(
            'main/admin/Teacher/_teacher_table.html',
            {'Teacher': books},
            request=request
        )
        return JsonResponse(data)


## список_заявок
class ListTeacher(DataMixin, ListView):
    model = CustomUser
    template_name = "main/admin/Teacher/list_teacher.html"
    context_object_name = "Teacher"
    queryset = CustomUser.objects.all().order_by("id")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Время")
        return dict(list(context.items()) + list(c_def.items()))

    def get(self, request, *args, **kwargs):
        for key in request.GET.keys():
            if key.startswith('btn_'):
                btn_pk = key[4:]
                record = CustomUser.objects.get(id=btn_pk)
                record.delete()
        return super(ListTeacher, self).get(request, *args, **kwargs)


## Создание кабинета
class UpdateTeacher(DataMixin, BSModalUpdateView):
    model = CustomUser
    form_class = UpdateTeacherForm
    template_name = 'main/admin/Teacher/update_teacher.html'
    success_url = reverse_lazy('list_teacher')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Укажите причину отклонения заявки")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            form.save()
        return super().form_valid(form)


## список зарезервированных лабораторий
class ListResCab(DataMixin, ListView):
    model = CustomUser
    template_name = "main/Teacher/reserved_pc.html"
    context_object_name = "Res_lab"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Зарезервированные лаборатории")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Reserved_Cabinet.objects.filter(Q(user_id=self.request.user)).order_by("-id")

    def get(self, request, *args, **kwargs):
        for key in request.GET.keys():
            if key.startswith('btn_'):
                btn_pk = key[4:]
                record = Reserved_Cabinet.objects.get(id=btn_pk)
                record.delete()
        return super(ListResCab, self).get(request, *args, **kwargs)