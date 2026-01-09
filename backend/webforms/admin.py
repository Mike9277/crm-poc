from django.contrib import admin
from .models import Webform, Website, WebformSubmission


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "external_id", "created_at")
    search_fields = ("name", "url", "external_id")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Webform)
class WebformAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "external_id", "created_at")
    search_fields = ("name", "external_id")
    list_filter = ("website", "created_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(WebformSubmission)
class WebformSubmissionAdmin(admin.ModelAdmin):
    list_display = ("webform", "person", "external_id", "created_at")
    search_fields = ("webform__name", "person__email", "external_id")
    list_filter = ("webform", "created_at", "source_website")
    readonly_fields = ("created_at", "updated_at")
