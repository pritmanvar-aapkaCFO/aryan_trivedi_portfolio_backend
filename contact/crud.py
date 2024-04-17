from django.db import InterfaceError, Error, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError
from contact.models import Contact
from utils.utils import commonResponse
from utils.notification import Email
from fastapi import status


def postContact(data, response):
    try:
        contact = Contact(name=data.name, email=data.email, message=data.message)
        contact.save()

        subject = "Regarding Contact Query"
        message = f'''We have recived following details with your contact request,
        
        Name: {data.name}
        Email: {data.email}
        Message: {data.message}
        
        We will contact you very soon, Thank you for your patience'''
        
        message_for_aryan = f'''Someone is trying to contact you through your portfolio.,
        
        Name: {data.name}
        Email: {data.email}
        Message: {data.message}
        
        We will contact you very soon, Thank you for your patience'''

        try:
            email = Email()
            res = email.send(subject=subject, message=message, recipient_list=[data.email])
            if(res['status'][0]['Error'] == 'False'):
                contact.is_email_send = True
                contact.save()
            res_aryan = email.send(subject=subject, message=message_for_aryan, recipient_list=["prit.manvar@aapkacfo.com"])
        except:
            pass
        
        response.status_code = status.HTTP_200_OK
        return commonResponse(200, "False", 0, "Contact details submitted.", Message="Contact details submitted.")

    except (InterfaceError, Error, Exception, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return commonResponse(500, "True", 0, "Something went wrong, Please try again.", Message=("{}").format(error))
