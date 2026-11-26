from django.contrib import admin

from .models import Photo, Tag

admin.site.register(Tag)
admin.site.register(Photo)
