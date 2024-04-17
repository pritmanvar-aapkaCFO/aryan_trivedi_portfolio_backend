from fastapi import APIRouter, Response
from utils.schemas import response
from contact.schemas import contact
from contact.crud import postContact
from utils.validation import ContactDataValidation
from utils.utils import commonResponse

contact_router = APIRouter()

@contact_router.post("", summary="post contact details", response_model=response)
def contact(data: contact, response: Response):
    isDataValid = ContactDataValidation(data)
    if isDataValid is not None:
        return commonResponse(500, "True", 0, isDataValid, Message=isDataValid)
    
    return postContact(data, response)