from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Yacht, Rental
from .forms import UserRegistrationForm


admin.site.register(Rental)
@admin.register(Yacht)
class YachtAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'price_per_day', 'capacity', 'availability']

    def availability(self, obj):
        return "Available" if obj.status == 'available' else "Unavailable"
    availability.short_description = 'Availability'



class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = UserRegistrationForm
    form = UserRegistrationForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'address')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
