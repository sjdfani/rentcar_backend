from django.contrib import admin
from .models import Reserve


class ReserveAdmin(admin.ModelAdmin):
    list_display = (
        "user", "start_rent_date", "reserve_status",
        "date_of_change_status", "paid_date", "payment_status",
    )
    list_filter = ("reserve_status", "payment_status")


admin.site.register(Reserve, ReserveAdmin)
