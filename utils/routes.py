from fastapi import APIRouter
from utils.schemas import sendOTP, verifyOTP, emailPhoneNumberVerify,response,verifyOtpResponse
from utils.crud import sendOtp, verifyOtp, isEmailPhoneNumberAvailable
from utils.utils import commonResponse,tokenResponse
from utils.validation import emailPhoneNumberVerifyDataValidation,sendOTPDataValidation,verifyOTPDataValidation
common_router = APIRouter()


@common_router.post("/sendOtp", summary="send OTP",response_model=response)
def sendOTP(data: sendOTP):
    isDataValid=sendOTPDataValidation(data)
    if isDataValid is not None:
        return commonResponse(200,"True",0,"Unacceptable Parameter Value",Message=isDataValid)
    return sendOtp(data)


@common_router.post("/verifyOtp", summary="verify OTP",response_model=verifyOtpResponse)
def verifyOTP(data: verifyOTP):
    isDataValid=verifyOTPDataValidation(data)
    if isDataValid is not None:
        return tokenResponse("","",200,"True",0,"Unacceptable Parameter Value",Message=isDataValid)
    return verifyOtp(data)


@common_router.post("/isEmailPhoneNumberAvailable", summary="check email and phone number available or not",response_model=response)
def verifyEmailPhoneNumber(data: emailPhoneNumberVerify):
    isDataValid=emailPhoneNumberVerifyDataValidation(data)
    if isDataValid is not None:
        return commonResponse(200,"True",0,"Unacceptable Parameter Value",Message=isDataValid)
    return isEmailPhoneNumberAvailable(data)
