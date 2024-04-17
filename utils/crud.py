from django.db import InterfaceError, Error, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError
import random

from django.core.cache import cache
from authentication.models import user
from utils.utils import create_access_token, create_refresh_token, commonResponse, tokenResponse, twoFactor, Email


# ****************************************************** send otp using sms ******************************************************


def sendSmsOtp(data):
    sms = twoFactor()
    return sms.send(data.phoneNumber)

# ****************************************************** send otp using email ******************************************************


def sendEmailOtp(data):
    OTP = random.randint(1000, 9999)
    emailotp = Email()
    cache.set(data.email, OTP)
    return emailotp.send("OTP Verification", "Here is your OTP : " +
                         str(OTP), [data.email])

# ****************************************************** send otp ******************************************************


def sendOtp(data):
    try:
        return sendSmsOtp(data)
    except Exception as e:
        return commonResponse(200, "True", 0, "", Message=str(e))

# ****************************************************** verify email otp ******************************************************


def verifyEmailOtp(data):
    if cache.get(data.email) == data.emailOTP:
        return True
    return False
# ****************************************************** verify sms otp ******************************************************


def verifySmsOtp(data):
    sms = twoFactor()
    isSmsOtpVerified = sms.verify(data.phoneNumber, data.phoneNumberOTP)
    return isSmsOtpVerified

# ****************************************************** verify otp ******************************************************


def verifyOtp(data):
    if verifySmsOtp(data):
        return tokenResponse(access_token=create_access_token(data.phoneNumber), refresh_token=create_refresh_token(data.phoneNumber), Response=200, Error="False", ErrorCode=0, ResponseMessage="", Message="OTP Matched")
    return tokenResponse(access_token="", refresh_token="", Response=200, Error="False", ErrorCode=0, ResponseMessage="", Message="OTP is incorrect!")


# ****************************************************** Email/Phone Number available or not******************************************************


def isEmailPhoneNumberAvailable(data):
    datatype = data.type
    try:
        if datatype == "email":
            dentistuser = user.objects.get(email=data.email)
            return commonResponse(200, "False", 0, "", Message=("Email Is Already In Use."))
        elif datatype == "phoneNumber":
            dentistuser = user.objects.get(phone_number=data.phoneNumber)
            return commonResponse(200, "False", 0, "", Message=("Phone Number Is Already in Use."))
        else:
            message = ""
            try:
                dentistuser = user.objects.get(email=data.email)
                message = message + " Email Is already In Use. "
            except:
                message = message + " Email Is Available. "
            try:
                dentistuser = user.objects.get(phone_number=data.phoneNumber)
                message = message + " Phone Number Is Already in Use. "
            except:
                message = message + " Phone Number is available. "
            return commonResponse(200, "False", 0, "", Message=message)
    except (InterfaceError, Error, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        return commonResponse(400, "True", 0, "", Message=("{}").format(error))

    except Exception as e:
        return commonResponse(200, "True", 0, "", Message=("{} Is Available.").format(datatype))
