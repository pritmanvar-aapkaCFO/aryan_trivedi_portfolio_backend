from typing import Sequence, Any
from pydantic import BaseModel, Field


class emailPhoneNumberVerify(BaseModel):
    email: str
    phoneNumber: int
    type: str

    class Config:
        orm_mode = True


class sendOTP(BaseModel):
    phoneNumber: int


class verifyOTP(BaseModel):
    phoneNumber: int
    phoneNumberOTP: int


class responseParameter(BaseModel):
    Response: int
    Error: str
    ErrorCode: int
    ResponseMessage: str
    Message: Any

    class Config:
        orm_mode = True


class response(BaseModel):
    status: Sequence[responseParameter]
    value: Any = None

    class Config:
        orm_mode = True


class tokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    status: Sequence[responseParameter]
    value: Any

    class Config:
        orm_mode = True


class verifyOtpResponse(BaseModel):
    access_token: str
    refresh_token: str
    status: Sequence[responseParameter]

    class Config:
        orm_mode = True


class userBase(BaseModel):
    firstName: str
    lastName: str
    email: str
    phoneNumber: int

    class Config:
        orm_mode = True
