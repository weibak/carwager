from django.contrib import admin
from news.models import News, Tags


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("title",)
    fields = ("title",)
    search_fields = ("title",)


class TagsAdminInline(admin.TabularInline):
    model = Tags.news.through


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "image", "slug", "created_at")
    fields = ("title", "image", "slug", "text", "created_at")
    readonly_fields = ("created_at",)
    search_fields = ("title", "slug", "text")

    inlines = (TagsAdminInline,)
