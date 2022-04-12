from django.contrib import admin

from .models import *



admin.site.register(CustomUser)
admin.site.register(Reserved_Cabinet)
admin.site.register(Cabinet)
admin.site.register(TimeInterval)
admin.site.register(Equipment)



