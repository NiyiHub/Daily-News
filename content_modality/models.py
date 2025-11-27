from django.db import models
from content_processing.models import PublishedContent
import uuid
from django.utils.timezone import now
from ckeditor.fields import RichTextField 

CATEGORY_CHOICES = [
    ('US', 'U.S'),
    ('WORLD', 'World'),
    ('POLITICS', 'Politics'),
    ('HEALTH', 'Health'),
    ('SCI_TECH', 'Science & Tech'),
    ('BUSINESS', 'Business'),
    ('LIFESTYLE', 'Lifestyle'),
    ('OPINION', 'Opinion'),
    ('MEDIA', 'Media'),
    ('SPORTS', 'Sports'),
    ('WEATHER', 'Weather'),
]

class UserSession(models.Model):
    """
    Model to store user session based on a unique User ID.
    """
    user_id = models.CharField(max_length=100, unique=True)
    session_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(default=now)

    def update_last_active(self):
        """Update the last active timestamp."""
        self.last_active = now()
        self.save()

    @staticmethod
    def create_session(user_id):
        """Create a new session or return an existing one."""
        session, created = UserSession.objects.get_or_create(user_id=user_id)
        if not created:
            session.update_last_active()
        return session

    def __str__(self):
        return f"UserSession: {self.user_id}"

# ---------------------------
# Bookmark Model
# ---------------------------
class UserBookmark(models.Model):
    """
    Model to track content bookmarked by users.
    """
    user = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name="bookmarks")
    content_id = models.CharField(max_length=255)
    content_type = models.CharField(max_length=50)  # e.g., Written, Video, WrittenImage
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user_id} bookmarked {self.content_type} - {self.content_id}"

# ---------------------------
# Interactive Models for Written Content
# ---------------------------
class WrittenContent(models.Model):
    published_content = models.OneToOneField(
        PublishedContent, 
        on_delete=models.CASCADE, 
        related_name="written_content"
    )
    title = models.CharField(max_length=999)  
    content = RichTextField(max_length=5000)  # Changed to RichTextField
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='US')

    def __str__(self):
        return f"WrittenContent: {self.title}"

class WrittenContentLike(models.Model):
    user = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name="written_likes")
    written_content = models.ForeignKey(WrittenContent, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

class WrittenContentComment(models.Model):
    user = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name="written_comments")
    written_content = models.ForeignKey(WrittenContent, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

class WrittenContentShare(models.Model):
    user = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name="written_shares")
    written_content = models.ForeignKey(WrittenContent, on_delete=models.CASCADE, related_name="shares")
    platform = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

# ---------------------------
# Interactive Models for Written+Image Content
# ---------------------------
class WrittenImageContent(models.Model):
    published_content = models.OneToOneField(
        PublishedContent, 
        on_delete=models.CASCADE, 
        related_name="written_image_content"
    )
    title = models.CharField(max_length=999)  
    content = RichTextField(max_length=5000)  # Changed to RichTextField
    image_url = models.URLField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='US')

    def __str__(self):
        return f"WrittenImageContent: {self.title}"

class WrittenImageContentLike(models.Model):
    user = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name="written_image_likes")
    written_image_content = models.ForeignKey(WrittenImageContent, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

class WrittenImageContentComment(models.Model):
    user = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name="written_image_comments")
    written_image_content = models.ForeignKey(WrittenImageContent, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

class WrittenImageContentShare(models.Model):
    user = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name="written_image_shares")
    written_image_content = models.ForeignKey(WrittenImageContent, on_delete=models.CASCADE, related_name="shares")
    platform = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

# ---------------------------
# Interactive Models for Video Content
# ---------------------------
class VideoContent(models.Model):
    published_content = models.OneToOneField(
        PublishedContent, 
        on_delete=models.CASCADE, 
        related_name="video_content"
    )
    title = models.CharField(max_length=999)  
    video_url = models.URLField(null=True, blank=True)  
    summary = RichTextField(max_length=200)  # Changed to RichTextField
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='US')

    def __str__(self):
        return f"VideoContent: {self.title}"

class VideoContentLike(models.Model):
    user = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name="video_likes")
    video_content = models.ForeignKey(VideoContent, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

class VideoContentComment(models.Model):
    user = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name="video_comments")
    video_content = models.ForeignKey(VideoContent, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

class VideoContentShare(models.Model):
    user = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name="video_shares")
    video_content = models.ForeignKey(VideoContent, on_delete=models.CASCADE, related_name="shares")
    platform = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)