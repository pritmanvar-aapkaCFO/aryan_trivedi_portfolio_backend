from django.db import InterfaceError, Error, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError
from myimages.models import Image, Video
from utils.utils import commonResponse
from fastapi import status


def getImages():
    try:
        images = Image.objects.all()
        videos = Video.objects.all().order_by('id')
        
        response_obj = {'images': [{'id': image.id, 'image': str(image.image)} for image in images],
                        'videos': [{'id': video.id, 'video': str(video.video), "yt_url": video.youtube_video_link} for video in videos]}
        return commonResponse(200, "False", 0, "Images fetched.", Message="Images fetched.", Value=response_obj)

    except (InterfaceError, Error, Exception, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        return commonResponse(500, "True", 0, "Something went wrong, Please try again.", Message=("{}").format(error))
