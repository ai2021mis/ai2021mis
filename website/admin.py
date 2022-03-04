from django.contrib import admin
from website.models import Gallery

# Register your models here.
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('filename', 'created_at')


admin.site.register(Gallery, GalleryAdmin)
