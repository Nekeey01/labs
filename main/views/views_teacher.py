from .imports import *

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
    template_name = 'main/admin/create_teacher.html'
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
