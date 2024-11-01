from django.contrib import admin

# Register your models here.

from .models import Question
from .models import Persona
from .models import Choice

admin.site.register(Question)
admin.site.register(Persona)
admin.site.register(Choice)
