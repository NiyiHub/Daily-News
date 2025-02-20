from django.db import models
from content_processing.models import PublishedContent

# ---------------------------
# Interactive Models for Written Content
# ---------------------------
class WrittenContent(models.Model):
    """
    Model for content rendered as a written article.
    """
    published_content = models.OneToOneField(
        PublishedContent, 
        on_delete=models.CASCADE, 
        related_name="written_content"
    )
    title = models.CharField(max_length=999)  # Title of the article
    content = models.TextField(max_length=2000)  # Article text content
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WrittenContent: {self.title}"

class WrittenContentLike(models.Model):
    written_content = models.ForeignKey(WrittenContent, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

class WrittenContentComment(models.Model):
    written_content = models.ForeignKey(WrittenContent, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

class WrittenContentShare(models.Model):
    written_content = models.ForeignKey(WrittenContent, on_delete=models.CASCADE, related_name="shares")
    platform = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


# ---------------------------
# Interactive Models for Written+Image Content
# ---------------------------
class WrittenImageContent(models.Model):
    """
    Model for content rendered as a written article with an image.
    """
    published_content = models.OneToOneField(
        PublishedContent, 
        on_delete=models.CASCADE, 
        related_name="written_image_content"
    )
    title = models.CharField(max_length=999)  # Title of the article
    content = models.TextField(max_length=2000)  # Article text content
    image_url = models.URLField(null=True, blank=True)  # Associated image URL
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WrittenImageContent: {self.title}"

class WrittenImageContentLike(models.Model):
    written_image_content = models.ForeignKey(WrittenImageContent, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

class WrittenImageContentComment(models.Model):
    written_image_content = models.ForeignKey(WrittenImageContent, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

class WrittenImageContentShare(models.Model):
    written_image_content = models.ForeignKey(WrittenImageContent, on_delete=models.CASCADE, related_name="shares")
    platform = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


# ---------------------------
# Interactive Models for Video Content
# ---------------------------
class VideoContent(models.Model):
    """
    Model for content rendered as a video with a summary.
    """
    published_content = models.OneToOneField(
        PublishedContent, 
        on_delete=models.CASCADE, 
        related_name="video_content"
    )
    title = models.CharField(max_length=999)  # Title for the video content
    video_url = models.URLField(null=True, blank=True)  # Video URL
    summary = models.TextField(max_length=200, help_text="Summary (50-70 words)")  # Video summary
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"VideoContent: {self.title}"

class VideoContentLike(models.Model):
    video_content = models.ForeignKey(VideoContent, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

class VideoContentComment(models.Model):
    video_content = models.ForeignKey(VideoContent, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

class VideoContentShare(models.Model):
    video_content = models.ForeignKey(VideoContent, on_delete=models.CASCADE, related_name="shares")
    platform = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
