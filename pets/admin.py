from django.utils.html import format_html
from django.contrib import admin
from .models import Pet, Photo, Ownership


# Register your models here.
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('pet', 'file_link')

    def file_link(self, obj):
        if obj.file:
            url = obj.file.url
            return format_html('<a href="{}" target="_blank">Download</a>', url)
        return "-"

    file_link.short_description = "File URL"


admin.site.register(Pet)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Ownership)
