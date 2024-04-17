from django.db import models

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to="image/")
    
    def __str__(self) -> str:
        return str(self.image)

class Video(models.Model):
    video = models.FileField(upload_to="video/")
    youtube_video_link = models.CharField(max_length=300, null=True, blank=True)
    
    def __str__(self) -> str:
        return str(self.video)