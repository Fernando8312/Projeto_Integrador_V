from django.contrib import admin

from .models import Worker, AccessRecord

admin.site.register(Worker)
admin.site.register(AccessRecord)