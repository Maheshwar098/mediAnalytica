from django.contrib import admin
from .models import DiseaseSpeciality
# Register your models here.
@admin.register(DiseaseSpeciality)
class DiseaseSpecialtyAdmin(admin.ModelAdmin):
    list_display = ('disease', 'speciality')
    search_fields = ('disease', 'speciality')

    def has_add_permission(self, request):
        # Control add permissions if needed
        return True

    def has_change_permission(self, request, obj=None):
        # Control change permissions if needed
        return True

    def has_delete_permission(self, request, obj=None):
        # Control delete permissions if needed
        return True