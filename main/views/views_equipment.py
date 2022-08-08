from .imports import *


## Создание ПО
class CreateEquipment(BSModalCreateView):
    template_name = 'main/admin/Equipment/create_equipment.html'
    form_class = UpdateEquipmentForm
    success_url = reverse_lazy('list_equipment')


def equips(request):
    data = dict()
    if request.method == 'GET':
        books = Equipment.objects.all()
        # asyncSettings.dataKey = 'table'
        data['tables'] = render_to_string(
            'main/admin/Equipment/_books_table.html',
            {'Equip': books},
            request=request
        )
        return JsonResponse(data)


## список ПО
class ListEquipment(DataMixin, ListView):
    model = Equipment
    template_name = "main/admin/Equipment/list_equipment.html"
    context_object_name = "Equip"
    queryset = Equipment.objects.all().order_by("title")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Список ПО")
        return dict(list(context.items()) + list(c_def.items()))

    def get(self, request, *args, **kwargs):
        for key in request.GET.keys():
            if key.startswith('btn_'):
                btn_pk = key[4:]
                record = Equipment.objects.get(id=btn_pk)
                record.delete()

        return super(ListEquipment, self).get(request, *args, **kwargs)


## Создание кабинета
class UpdateEquipment(DataMixin, BSModalUpdateView):
    model = Equipment
    form_class = UpdateEquipmentForm
    template_name = 'main/admin/Equipment/update_equipment.html'
    success_url = reverse_lazy('list_equipment')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Укажите причину отклонения заявки")
        return dict(list(context.items()) + list(c_def.items()))




