from django.contrib import admin
from .models import Post, Image

admin.site.register(Image)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'tag_list']

    def tag_list(self, obj):
        return ", ".join(o for o in obj.tags.names())
