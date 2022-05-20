from .imports import *


## вьюха главной странички


class Index(DataMixin, ListView):
    model = Cabinet
    template_name = "main/index.html"
    context_object_name = "po"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Главная!", count_lab=Cabinet.objects.count(),
                                      res_lab=Reserved_Cabinet.objects.count())
        return dict(list(context.items()) + list(c_def.items()))

    ## получает список тасков, начиная с последнего созданного
    def get_queryset(self):
        return Equipment.objects.order_by('-id')







