from .imports import *

## Создание интервалов времени
class CreateTimeInterval(BSModalCreateView):
    form_class = UpdateIntervalForm
    template_name = 'main/admin/Time_interval/create_time_inteval.html'
    success_url = reverse_lazy('list_times')

def times(request):
    data = dict()
    if request.method == 'GET':
        books = TimeInterval.objects.all()
        # asyncSettings.dataKey = 'table'
        data['tables'] = render_to_string(
            'main/admin/Time_interval/_time_table.html',
            {'Time': books},
            request=request
        )
        return JsonResponse(data)


## список интервалов времени
class ListTime(DataMixin, ListView):
    model = TimeInterval
    template_name = "main/admin/Time_interval/list_times.html"
    context_object_name = "Time"
    queryset = TimeInterval.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Время")
        return dict(list(context.items()) + list(c_def.items()))

    def get(self, request, *args, **kwargs):
        for key in request.GET.keys():
            if key.startswith('btn_'):
                btn_pk = key[4:]
                record = TimeInterval.objects.get(id=btn_pk)
                record.delete()

        return super(ListTime, self).get(request, *args, **kwargs)


## Обновление интервала времени
class UpdateTime(DataMixin, BSModalUpdateView):
    model = TimeInterval
    form_class = UpdateIntervalForm
    template_name = 'main/admin/Time_interval/update_time.html'
    success_url = reverse_lazy('list_times')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Укажите причину отклонения заявки")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            form.save()
        return super().form_valid(form)

