
## Контекстное меню (которое сверху). title - заголовок. url_name - ссылка странички. path - та же url_name,
# только с '/' для проверки, на той ли мы страничке находимся
menu = [{'title': 'Главная', 'url_name': 'home', 'path': '/'},
        {'title': 'Посмотреть лаборатории', 'url_name': 'show_pc', 'path': '/show_pc'},
        {'title': 'Добавить лабораторию', 'url_name': 'create_cab', 'path': '/create_cab'},
        {'title': 'Добавить время', 'url_name': 'create_time_interval', 'path': '/create_time_interval'},
        {'title': 'Загрузить преподавателей', 'url_name': 'load_teacher', 'path': '/load_teacher'},
        {'title': 'Добавить ПО', 'url_name': 'create_equipment', 'path': '/create_equipment'},
        {'title': 'Добавить преподавателя', 'url_name': 'create_teacher', 'path': '/create_teacher'},
        ]

class DataMixin:
    def get_user_content(self, **kwargs):
        context = kwargs
        context['error'] = ''
        context['menu'] = menu
        return context