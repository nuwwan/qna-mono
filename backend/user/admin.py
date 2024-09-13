from django.contrib import admin
from .models import Tag, Subject, Topic, Profile

# Register your models here.
admin.site.register(Tag)
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(Profile)
