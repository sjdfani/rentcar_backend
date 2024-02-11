from django.contrib import admin
from .models import Category, CarOptions, CarYear, CarModel, Color, Car


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "id")
    list_editable = ("status",)


class CarOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "id")
    list_editable = ("status",)


class CarYearAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "id")
    list_editable = ("status",)


class CarModelAdmin(admin.ModelAdmin):
    list_display = ("manufacturers", "name", "id", "pk")


class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "id")
    list_editable = ("status",)


class CarAdmin(admin.ModelAdmin):
    list_display = ("owner", "status", "id")
    list_editable = ("status",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(CarOptions, CarOptionAdmin)
admin.site.register(CarYear, CarYearAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Car, CarAdmin)
