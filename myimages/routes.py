from fastapi import APIRouter, Response
from myimages.crud import getImages
from utils.schemas import response


image_router = APIRouter()

@image_router.get("", summary="get images", response_model=response)
def contact():
    return getImages()