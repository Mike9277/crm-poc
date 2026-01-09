from django.contrib import admin
from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "source_website", "created_at")
    search_fields = ("email", "first_name", "last_name")