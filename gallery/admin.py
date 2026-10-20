from django.contrib import admin

from .models import Artwork, Exhibition


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ("title", "creation_date", "is_featured", "is_published")
    list_filter = ("is_featured", "is_published", "creation_date")
    search_fields = ("title", "description", "materials", "creation_location")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at",)


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ("title", "start_date", "end_date", "location", "is_published")
    list_filter = ("is_published", "start_date")
    search_fields = ("title", "description", "location")
    date_hierarchy = "start_date"
