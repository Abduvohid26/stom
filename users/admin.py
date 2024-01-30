from django.contrib import admin
from .models import User, Patients, Payments
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ('username',)

class PatientsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone')
    search_fields = ('first_name', 'last_name', 'phone', 'rengen_number')

class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('patient', 'amount')


admin.site.register(Patients, PatientsAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Payments, PaymentsAdmin)