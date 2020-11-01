from django.contrib import admin

from url_mangler.apps.url_mapper.models import UrlMapping


class UrlMappingAdmin(admin.ModelAdmin):
    pass


admin.site.register(UrlMapping, UrlMappingAdmin)
