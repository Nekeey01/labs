from .imports import *


# писок заявок
class ShowZayvkaFromUcheb(DataMixin, ListView):
    model = Zayavka
    template_name = "main/ucheb/list_zayvka_from_ucheb.html"
    context_object_name = "Zayavka"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Список заявок")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Zayavka.objects.filter(Q(status="Одобрено инф отделом")).order_by('-id')

    def get(self, request, *args, **kwargs):
        for key in request.GET.keys():
            if key.startswith('btn_'):
                btn_pk = key[4:]
                record = Zayavka.objects.get(id=btn_pk)
                record.status = "Одобрено"
                record.save()

                res_cab = Reserved_Cabinet(reserv_date=record.reserv_date, reserv_time=record.reserv_time,
                                           cab=record.zayavka_cab,
                                           user_id=record.zayavka_user_id)
                res_cab.save()

        return super(ShowZayvkaFromUcheb, self).get(request, *args, **kwargs)


# журнал всех заявок
class ShowJournal(DataMixin, ListView):
    model = Zayavka
    template_name = "main/ucheb/journal.html"
    context_object_name = "Journal"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Журнал всех заявок")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Zayavka.objects.all().order_by('-id')

    def get(self, request, *args, **kwargs):
        for key in request.GET.keys():
            if key.startswith('btn_'):
                btn_pk = key[4:]
                record = Zayavka.objects.get(id=btn_pk)
                record.delete()

        return super(ShowJournal, self).get(request, *args, **kwargs)


## убновление заявки
class UpdateZayvkaFromUcheb(DataMixin, BSModalUpdateView):
    model = Zayavka
    form_class = UpdateZayvkaForm
    template_name = 'main/ucheb/update_zayvka_from_ucheb.html'
    success_url = reverse_lazy('list_zayvka_from_ucheb')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Укажите причину отклонения заявки")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.status = "Отклонена"
        form.save()
        response = super().form_valid(form)
        return response

import datetime

## Аналитика
class Analitics(DataMixin, TemplateView):
    template_name = 'main/analitics/analitics.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.date.today()
        c_def = self.get_user_content(title="Аналитика",
                                      all_time_label=Reserved_Cabinet.objects.all().values_list('reserv_date',
                                                                                                flat=True).distinct().order_by(
                                          'reserv_date'),
                                      all_time_data=Reserved_Cabinet.objects.values('reserv_date').annotate(
                                          count_reslabs=Count('reserv_date')).order_by('reserv_date'),

                                      years_label=Reserved_Cabinet.objects.filter(
                                          reserv_date__year=today.year).values_list('reserv_date',
                                                                                    flat=True).distinct().order_by(
                                          'reserv_date'),
                                      years_data=Reserved_Cabinet.objects.filter(reserv_date__year=today.year).values(
                                          'reserv_date').annotate(count_reslabs=Count('reserv_date')).order_by(
                                          'reserv_date'),

                                      month_label=Reserved_Cabinet.objects.filter(reserv_date__year=today.year,
                                                                                  reserv_date__month=today.month).values_list(
                                          'reserv_date', flat=True).distinct().order_by('reserv_date'),
                                      month_data=Reserved_Cabinet.objects.filter(reserv_date__year=today.year,
                                                                                 reserv_date__month=today.month).values(
                                          'reserv_date').annotate(count_reslabs=Count('reserv_date')).order_by(
                                          'reserv_date'),

                                      qss=Zayavka.objects.all().values_list('status', flat=True).distinct().order_by(
                                          "status"),
                                      qss2=Zayavka.objects.values('status').annotate(
                                          count_zayavok=Count('status')).order_by("status"))
        return dict(list(context.items()) + list(c_def.items()))
