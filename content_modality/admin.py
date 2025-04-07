from django.contrib import admin
from .models import (
    UserSession,
    UserBookmark,
    
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

# ---- User Session & Bookmark Admin ----
@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'session_token', 'created_at', 'last_active')
    search_fields = ('user_id',)

@admin.register(UserBookmark)
class UserBookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_id', 'content_type', 'created_at')
    search_fields = ('user__user_id', 'content_id')

# ---- Written Content Admin ----
@admin.register(WrittenContent)
class WrittenContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_content', 'category', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('category',)

@admin.register(WrittenContentLike)
class WrittenContentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'written_content', 'created_at')
    search_fields = ('user__user_id',)

@admin.register(WrittenContentComment)
class WrittenContentCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'written_content', 'text', 'created_at')
    search_fields = ('user__user_id', 'text')

@admin.register(WrittenContentShare)
class WrittenContentShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'written_content', 'platform', 'created_at')
    search_fields = ('user__user_id', 'platform')

# ---- WrittenImageContent Admin ----
@admin.register(WrittenImageContent)
class WrittenImageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_content', 'category', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('category',)

@admin.register(WrittenImageContentLike)
class WrittenImageContentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'written_image_content', 'created_at')
    search_fields = ('user__user_id',)

@admin.register(WrittenImageContentComment)
class WrittenImageContentCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'written_image_content', 'text', 'created_at')
    search_fields = ('user__user_id', 'text')

@admin.register(WrittenImageContentShare)
class WrittenImageContentShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'written_image_content', 'platform', 'created_at')
    search_fields = ('user__user_id', 'platform')

# ---- Video Content Admin ----
@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_content', 'category', 'created_at')
    search_fields = ('title',)
    list_filter = ('category',)

@admin.register(VideoContentLike)
class VideoContentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'video_content', 'created_at')
    search_fields = ('user__user_id',)

@admin.register(VideoContentComment)
class VideoContentCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'video_content', 'text', 'created_at')
    search_fields = ('user__user_id', 'text')

@admin.register(VideoContentShare)
class VideoContentShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'video_content', 'platform', 'created_at')
    search_fields = ('user__user_id', 'platform')
