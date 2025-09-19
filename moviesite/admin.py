from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Genre, Movie, Comment, Profile

admin.site.register(Profile)

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
    list_display_links = ('id', 'type')
    search_fields = ('type',)
    ordering = ('type',)

    fields = ('type',)

class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'director', 'genre', 'release', 'author', 'published', 'get_image')
    list_display_links = ('id', 'title', 'get_image')
    search_fields = ('title', 'description')
    list_filter = ('genre', 'release')
    list_editable = ('director', 'genre', 'author', 'published')
    inlines = [
        CommentInline
    ]

    def get_image(self, obj: Movie):
        if obj.cover:
            return mark_safe(f"<img src='{obj.cover.url}' width='60px' />")
        return "No Image"
    get_image.short_description = "Cover"

    fieldsets = (
        ("Ma'lumotlar", {
            'fields': ('title', 'director', 'description', 'genre'),
        }),
        ("Media fayllar", {
            'fields': ('cover', 'video')
        }),
        ("Qo‘shimcha", {
            'fields': ('release', 'published')
        }),
    )

admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)