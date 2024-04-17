import re


class validate:

    def __init__(self, string):
        self.string = str(string)

    def Email(self):
        ptn = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        return re.match(ptn, str(self.string))

    def PhoneNumber(self):
        ptn = "^[6-9]\d{9}$"
        return re.match(ptn, str(self.string))

    def password(self):
        ptn = re.compile(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
        return re.match(ptn, self.string)

    def date(self):
        ptn = re.compile(
            "/^\d{4}(\-)(((0)[0-9])|((1)[0-2]))(\-)([0-2][0-9]|(3)[0-1])$/gm")
        return re.match(ptn, self.string)

    def length(self, min_length: int, max_length: int):
        length = len(self.string)
        if length >= min_length and length <= max_length:
            return True
        return False

    def trueOrFalse(self):
        ptn = r"^true$|^false$"
        return re.match(ptn, str(self.string).lower())

    def emailOrPhoneNumberOrBoth(self):
        ptn = "^email$|^phoneNumber$|^both$"
        return re.match(ptn, self.string)


def resetPasswordDataValidation(data):
    Error = dict()
    try:
        if not validate(data.email).Email():
            Error["email Value Error"] = "Incorrect Email Format."
            return Error

        if not validate(data.newPassword).password():
            Error["newPassword Value Error"] = "Must Be Contains Uppercase, Lowercase Letters, Numbers, Special Characters And Length Is Greater Than 8 Character And Less Then 16 Character."
            return Error
    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error

    return None


def changePasswordDataValidation(data):
    Error = dict()
    try:
        # if not validate(data.email).Email():
        #     Error["email Value Error"] = "Incorrect Email Format."
        #     return Error

        if not validate(data.oldPassword).password():
            Error["oldPassword Value Error"] = "Must Be Contains Uppercase, Lowercase Letters, Numbers, Special Characters And Length Is Greater Than 8 Character And Less Then 16 Character."
            return Error

        if not validate(data.newPassword).password():
            Error["newPassword Value Error"] = "Must Be Contains Uppercase, Lowercase Letters, Numbers, Special Characters And Length Is Greater Than 8 Character And Less Then 16 Character."
            return Error
    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error

    return None


def loginDataValidation(data):
    Error = dict()
    try:
        if not validate(data.email).Email():
            Error["email Value Error"] = "Incorrect Email Format."
            return Error

        if not validate(data.password).password():
            Error["Password Value Error"] = "Must Be Contains Uppercase, Lowercase Letters, Numbers, Special Characters And Length Is Greater Than 8 Character And Less Then 16 Character."
            return Error
    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error

    return None


def paymentDataValidation(data):
    Error = dict()
    try:
        if not validate(data.email).Email():
            Error["email Value Error"] = "Incorrect Email Format."
            return Error

    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error

    return None


def emailPhoneNumberVerifyDataValidation(data):
    Error = dict()
    try:
        if not validate(data.type).emailOrPhoneNumberOrBoth():
            Error["type Value Error"] = "Either An 'email' Or 'phoneNumber' Or 'both' Are Expected Strings."
            return Error
        else:
            if data.type == "email":
                if not validate(data.email).Email():
                    Error["email Value Error"] = "Incorrect Email Format."
                    return Error
            elif data.type == "phoneNumber":
                if not validate(data.phoneNumber).PhoneNumber():
                    Error["phoneNumber Value Error"] = "Incorrect Phone Number Format."
                    return Error
            else:
                if not validate(data.phoneNumber).PhoneNumber():
                    Error["phoneNumber Value Error"] = "Incorrect Phone Number Format."
                    return Error
                if not validate(data.email).Email():
                    Error["email Value Error"] = "Incorrect Email Format."
                    return Error
    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error

    return None


def sendOTPDataValidation(data):
    Error = dict()

    if not validate(data.phoneNumber).PhoneNumber():
        Error["phoneNumber Value Error"] = "Incorrect Phone Number Format."
        return Error

    return None


def verifyOTPDataValidation(data):
    Error = dict()
    try:

        if not validate(data.phoneNumber).PhoneNumber():
            Error["phoneNumber Value Error"] = "Incorrect Phone Number Format."
            return Error
    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error
    return None


def ContactDataValidation(data):
    Error = dict()
    try:        
        if not validate(data.name).length(0, 70):
            Error = "Length of Name Must Be Less Then 70."
            return Error

        if not validate(data.email).Email():
            Error = "Incorrect Email Format."
            return Error

    except AttributeError as e:
        Error = str(e)
        return Error

    except Exception as e:
        Error = str(e)
        return Error

    return None