from django.contrib import admin
from myimages.models import Image, Video


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "image")

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "video")
