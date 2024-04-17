from datetime import datetime, timedelta
from sre_parse import TYPE_FLAGS
from typing import Union, Any
from fastapi import Depends, HTTPException, status
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPException
from pydantic import BaseModel
import requests
import config
import json
from twilio.rest import Client
import typing as t
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
import random

def create_access_token(subject: Union[str, Any], expires_delta: int = config.settings.ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    try:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(
            to_encode, config.settings.JWT_SECRET_KEY, config.settings.ALGORITHM)
        return encoded_jwt
    except Exception as e:
        return str(e)


def create_refresh_token(subject: Union[str, Any], expires_delta: int = config.settings.REFRESH_TOKEN_EXPIRE_MINUTES) -> str:
    try:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(
            to_encode, config.settings.JWT_REFRESH_SECRET_KEY, config.settings.ALGORITHM)
        return encoded_jwt
    except Exception as e:
        return str(e)


def verify_access_token(jwt_token: str) -> bool:
    try:
        decoded_jwt = jwt.decode(
            jwt_token, config.settings.JWT_SECRET_KEY, config.settings.ALGORITHM)
        return {'verified': True, 'email': decoded_jwt['sub']}
    except (ExpiredSignatureError, Exception, InvalidSignatureError) as e:
        print(e)
        return {'verified': False, 'email': ''}


def commonResponse(Response: int, Error: str, ErrorCode: int, ResponseMessage: str, Message: Any, Value: Any = None):
    return {
        "status": [{
            "Response": Response,
            "Error": Error,
            "ErrorCode": ErrorCode,
            "ResponseMessage": ResponseMessage,
            "Message": Message
        }],
        "value": Value
    }


def tokenResponse(access_token: str, refresh_token: str, Response: int, Error: str, ErrorCode: int, ResponseMessage: str, Message: str, Value: Any = None):
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "status": [{
            "Response": Response,
            "Error": Error,
            "ErrorCode": ErrorCode,
            "ResponseMessage": ResponseMessage,
            "Message": Message

        }],
        "value": Value
    }


def paymentResponse(order: dict, Response: int, Error: str, ErrorCode: int, ResponseMessage: str, Message: str):
    return {
        "order": order,
        "status": [{
            "Response": Response,
            "Error": Error,
            "ErrorCode": ErrorCode,
            "ResponseMessage": ResponseMessage,
            "Message": Message
        }]
    }


def productResponce(products: dict, singleProduct: bool, Response: int, Error: str, ErrorCode: int, ResponseMessage: str, Message: Any):
    return {
        'products': products,
        'singleProduct': singleProduct,
        'status': [{
            'Response': Response,
            'Error': Error,
            'ErrorCode': ErrorCode,
            'ResponseMessage': ResponseMessage,
            "Message": Message
        }]
    }


def addedItemResponse(cart: dict, Response: int, Error: str, ErrorCode: int, ResponseMessage: str, Message: Any):
    return {
        'cart': cart,
        'status': [{
            'Response': Response,
            'Error': Error,
            'ErrorCode': ErrorCode,
            'ResponseMessage': ResponseMessage,
            "Message": Message
        }]
    }


def serviceResponse(service: dict, Response: int, Error: str, ErrorCode: int, ResponseMessage: str, Message: Any):
    return {
        'service': service,
        'status': [{
            'Response': Response,
            'Error': Error,
            'ErrorCode': ErrorCode,
            'ResponseMessage': ResponseMessage,
            "Message": Message
        }]
    }


def inquiryResponse(inquiries: dict, Response: int, Error: str, ErrorCode: int, ResponseMessage: str, Message: Any):
    return {
        'inquiries': inquiries,
        'status': [{
            'Response': Response,
            'Error': Error,
            'ErrorCode': ErrorCode,
            'ResponseMessage': ResponseMessage,
            "Message": Message
        }]
    }


def supportTicketResponse(support_ticket: dict, Response: int, Error: str, ErrorCode: int, ResponseMessage: str, Message: Any):
    return {
        'support_ticket': support_ticket,
        'status': [{
            'Response': Response,
            'Error': Error,
            'ErrorCode': ErrorCode,
            'ResponseMessage': ResponseMessage,
            "Message": Message
        }]
    }


def userResponse(user_res: dict, Response: int, Error: str, ErrorCode: int, ResponseMessage: str, Message: Any):
    return {
        'user': user_res,
        'status': [{
            'Response': Response,
            'Error': Error,
            'ErrorCode': ErrorCode,
            'ResponseMessage': ResponseMessage,
            "Message": Message
        }]
    }
    

def otpResponse(token: str, Response: int, Error: str, ErrorCode: int, ResponseMessage: str, Message: str, Value: Any = None):
    return {
        "token": token,
        "status": [{
            "Response": Response,
            "Error": Error,
            "ErrorCode": ErrorCode,
            "ResponseMessage": ResponseMessage,
            "Message": Message

        }],
        "value": Value
    }

# ****************************************************** Authorization Module ******************************************************


class UnauthorizedMessage(BaseModel):
    detail: str = "Unauthenticated User, Please login first."


get_bearer_token = HTTPBearer(auto_error=False)


async def get_token(
        auth: t.Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),) -> str:

    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UnauthorizedMessage().detail,
        )

    verification = verify_access_token(auth.credentials)
    if not verification['verified']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UnauthorizedMessage().detail,
        )

    return {'token': auth.credentials, 'email': verification['email']}


# ****************************************************** 2Factor sms sender ******************************************************


class twoFactor():

    def send(self, phoneNumber):
        try:
            smsOtp = requests.get(("https://2factor.in/API/V1/{api}/SMS/:+91{number}/AUTOGEN3/:otp_template_name").format(
                api=config.settings.SMSAPI, number=str(phoneNumber)))
            responseTxt = smsOtp.text
            json_acceptable_string = responseTxt.replace('"', "\"")
            smsResData = json.loads(json_acceptable_string)
            if smsResData["Status"] == "Error":
                return commonResponse(200, "True", 0, "", Message=smsResData["Details"])
            return commonResponse(200, "False", 0, "", Message="SMS sent successfully.")
        except Exception as e:
            return commonResponse(200, "True", 0, "", Message=str(e))

    def verify(self, phoneNumber, OTP):
        verifySmsOtp = requests.get(("https://2factor.in/API/V1/{api}/SMS/VERIFY3/91{phone_number}/{otp_entered_by_user}").format(
            api=config.settings.SMSAPI, phone_number=phoneNumber, otp_entered_by_user=OTP))
        responseTxt = verifySmsOtp.text
        json_acceptable_string = responseTxt.replace('"', "\"")
        smsResData = json.loads(json_acceptable_string)
        if smsResData['Details'] == "OTP Matched":
            return True
        return False

# ******************************************************  email sender ******************************************************


class Email():
    def send(self, subject, message, recipient_list):
        try:
            emailOtp = send_mail(
                subject,       # subject
                message,  # message
                config.settings.EMAIL_HOST_USER,    # from_email
                recipient_list           # recipient_list
            )
            print(emailOtp)
            return commonResponse(200, "False", 0, "", Message="Email Sent Successfully.")

        except BadHeaderError:              # If mail's Subject is not properly formatted.
            return commonResponse(400, "True", 0, "", Message="Invalid Header Found.")

        except SMTPException as e:          # It will catch other errors related to SMTP.
            print(e)
            return commonResponse(400, "True", 0, "", Message='There Was an Error Sending an Email.' + str(e))
        except:
            return commonResponse(200, "True", 0, "", Message="Failure In Sending Mail!")


# ******************************************************  whatsapp message sender ******************************************************

def send_whatsapp_notification(number, message):
    account_sid = config.settings.TWILIO_ACCOUNT_SID
    auth_token = config.settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=('whatsapp:+91{}').format(number)
    )

# ******************************************************  Generate OTP ******************************************************

def generate_otp():
    otp = random.randint(100000, 999999)  # Generate a random 6-digit OTP
    return otp
