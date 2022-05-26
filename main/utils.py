
#TODO: views.py,

#TODO: сделать шаблоны
#TODO: admin.py
#TODO: изменить резервацию в view
#TODO: добавить роли
#TODO: изменить отображение в профиле
#TODO: добавить мульти-список как в админке

#TODO: DOP_ одальное окно с объяснением причины отказа
#TODO: страничка для отображения заявок

## Контекстное меню (которое сверху). title - заголовок. url_name - ссылка странички. path - та же url_name,
# только с '/' для проверки, на той ли мы страничке находимся
menu = [{'title': 'Главная', 'url_name': 'home', 'path': '/'},
        {'title': 'Посмотреть лаборатории', 'url_name': 'show_pc', 'path': '/show_pc'},
        {'title': 'Добавить лабораторию', 'url_name': 'list_cab', 'path': '/list_cab'},
        {'title': 'Добавить время', 'url_name': 'list_times', 'path': '/list_times'},
        {'title': 'Добавить оборудование', 'url_name': 'list_oborud', 'path': '/list_oborud'},
        {'title': 'Добавить ПО', 'url_name': 'list_equipment', 'path': '/list_equipment'},
        {'title': 'Добавить преподавателя', 'url_name': 'list_teacher', 'path': '/list_teacher'},
        {'title': 'Список заявок как учеб', 'url_name': 'list_zayvka_from_ucheb', 'path': '/list_zayvka_from_ucheb'},
        {'title': 'Список заявок как инф', 'url_name': 'list_zayvka_from_inf', 'path': '/list_zayvka_from_inf'},
        {'title': 'Список заявок', 'url_name': 'list_users_zayavka', 'path': '/list_users_zayavka'},
        {'title': 'Заказанные лаборатории', 'url_name': 'reserved_cab', 'path': '/reserved_cab'},
        {'title': 'Журнал заявок', 'url_name': 'journal_zayavok', 'path': '/journal_zayavok'},
        {'title': 'Аналитика', 'url_name': 'analitic', 'path': '/analitic'},
        ]

class DataMixin:
    def get_user_content(self, **kwargs):
        context = kwargs
        context['error'] = ''
        context['menu'] = menu
        return context