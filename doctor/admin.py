from django.contrib import admin
from .models import Doctor
# Register your models here.
@admin.register(Doctor)
class DiseaseSpecialtyAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'speciality')
    search_fields = ('first_name', 'last_name', 'speciality')

    def has_add_permission(self, request):
        # Control add permissions if needed
        return True

    def has_change_permission(self, request, obj=None):
        # Control change permissions if needed
        return True

    def has_delete_permission(self, request, obj=None):
        # Control delete permissions if needed
        return True