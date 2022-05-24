from .imports import *


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
        title = form.cleaned_data['title']
        for i in Soft.objects.all():
            if title == i.title:
                i.count += form.cleaned_data["count"]
                i.save()
                return HttpResponseRedirect(self.success_url)
        form.save()
        return HttpResponseRedirect(self.success_url)


        form.instance.status = "Отклонена"
        form.save()
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('list_zayvka_from_inf')

