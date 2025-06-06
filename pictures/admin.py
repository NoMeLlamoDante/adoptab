from django.contrib import admin
from django.utils.html import format_html

from .models import Picture


# Register your models here.
class PictureAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_link')

    def file_link(self, obj):
        if obj.file:
            url = obj.file.url
            return format_html('<a href="{}" target="_blank">Download</a>', url)
        return "-"

    file_link.short_description = "File URL"


admin.site.register(Picture, PictureAdmin)
