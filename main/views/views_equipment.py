from .imports import *


## Создание ПО
class CreateEquipment(DataMixin, CreateView):
    form_class = CreateEquipmentForm
    template_name = 'main/admin/Equipment/create_equipment.html'
    success_url = reverse_lazy('create_equipment')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Добавить ПО")
        return dict(list(context.items()) + list(c_def.items()))


def books(request):
    data = dict()
    if request.method == 'GET':
        books = Equipment.objects.all()
        # asyncSettings.dataKey = 'table'
        data['tables'] = render_to_string(
            'main/_books_table.html',
            {'Equip': books},
            request=request
        )
        return JsonResponse(data)


## список_заявок
class ListEquipment(DataMixin, ListView):
    model = Equipment
    template_name = "main/admin/Equipment/list_equipment.html"
    context_object_name = "Equip"
    queryset = Equipment.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Список ПО")
        return dict(list(context.items()) + list(c_def.items()))


## Создание кабинета
class UpdateEquipment(DataMixin, BSModalUpdateView):
    model = Equipment
    form_class = UpdateEquipmentForm
    template_name = 'main/admin/Equipment/update_equipment.html'
    success_message = 'DDDDDDDDDDD.'
    success_url = reverse_lazy('list_equipment')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Укажите причину отклонения заявки")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            form.save()
        return super().form_valid(form)


