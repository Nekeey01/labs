from .imports import *

## Создание пользователя
class CreateOborud(BSModalCreateView):
    form_class = UpdateOborudForm
    template_name = 'main/admin/Oborud/create_oborud.html'
    success_url = reverse_lazy('list_oborud')


def oborud(request):
    data = dict()
    if request.method == 'GET':
        books = Oborud.objects.all()
        # asyncSettings.dataKey = 'table'
        data['tables'] = render_to_string(
            'main/admin/Oborud/_oborud_table.html',
            {'Oborud': books},
            request=request
        )
        return JsonResponse(data)


## список_заявок
class ListOborud(DataMixin, ListView):
    model = Oborud
    template_name = "main/admin/Oborud/list_oborud.html"
    context_object_name = "Oborud"
    queryset = Oborud.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Время")
        return dict(list(context.items()) + list(c_def.items()))

    def get(self, request, *args, **kwargs):
        for key in request.GET.keys():
            if key.startswith('btn_'):
                btn_pk = key[4:]
                record = Oborud.objects.get(id=btn_pk)
                record.delete()
        return super(ListOborud, self).get(request, *args, **kwargs)


## Создание кабинета
class UpdateOborud(DataMixin, BSModalUpdateView):
    model = Oborud
    form_class = UpdateOborudForm
    template_name = 'main/admin/Oborud/update_oborud.html'
    success_url = reverse_lazy('list_oborud')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Укажите причину отклонения заявки")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            form.save()
        return super().form_valid(form)
