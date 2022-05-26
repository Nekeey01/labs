from .imports import *



## регистрация пользователя
class RegisterUser(DataMixin, BSModalCreateView):
    form_class = CreateUserForm
    template_name = 'main/admin/create_user.html'
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


## Вьюха профиля
class Profile(DataMixin, UpdateView):
    model = CustomUser
    template_name = 'main/Teacher/profile.html'
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

# Список заявок пользователя
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