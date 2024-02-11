from django.contrib import admin
from .models import City


class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "id")
    list_filter = ("status",)


admin.site.register(City, CityAdmin)
