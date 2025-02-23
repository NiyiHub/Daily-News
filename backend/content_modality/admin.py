from django.contrib import admin
from .models import (
    WrittenContent,
    WrittenContentLike, 
    WrittenContentComment, 
    WrittenContentShare,

    WrittenImageContent, 
    WrittenImageContentLike, 
    WrittenImageContentComment, 
    WrittenImageContentShare,

    VideoContent, 
    VideoContentLike, 
    VideoContentComment, 
    VideoContentShare
)

@admin.register(WrittenContent)
class WrittenContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_content', 'created_at')
    search_fields = ('title', 'content')

@admin.register(WrittenContentLike)
class WrittenContentLikeAdmin(admin.ModelAdmin):
    list_display = ('written_content', 'created_at')

@admin.register(WrittenContentComment)
class WrittenContentCommentAdmin(admin.ModelAdmin):
    list_display = ('written_content', 'text', 'created_at')

@admin.register(WrittenContentShare)
class WrittenContentShareAdmin(admin.ModelAdmin):
    list_display = ('written_content', 'platform', 'created_at')


@admin.register(WrittenImageContent)
class WrittenImageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_content', 'created_at')
    search_fields = ('title', 'content')

@admin.register(WrittenImageContentLike)
class WrittenImageContentLikeAdmin(admin.ModelAdmin):
    list_display = ('written_image_content', 'created_at')

@admin.register(WrittenImageContentComment)
class WrittenImageContentCommentAdmin(admin.ModelAdmin):
    list_display = ('written_image_content', 'text', 'created_at')

@admin.register(WrittenImageContentShare)
class WrittenImageContentShareAdmin(admin.ModelAdmin):
    list_display = ('written_image_content', 'platform', 'created_at')


@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_content', 'created_at')
    search_fields = ('title',)

@admin.register(VideoContentLike)
class VideoContentLikeAdmin(admin.ModelAdmin):
    list_display = ('video_content', 'created_at')

@admin.register(VideoContentComment)
class VideoContentCommentAdmin(admin.ModelAdmin):
    list_display = ('video_content', 'text', 'created_at')

@admin.register(VideoContentShare)
class VideoContentShareAdmin(admin.ModelAdmin):
    list_display = ('video_content', 'platform', 'created_at')
