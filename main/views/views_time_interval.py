from .imports import *

## Создание интервалов времени
class CreateTimeInterval(DataMixin, CreateView):
    form_class = CreateTimeIntervalForm
    template_name = 'main/admin/create_time_inteval.html'
    success_url = reverse_lazy('create_time_interval')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Добавить интервал времени")
        return dict(list(context.items()) + list(c_def.items()))
