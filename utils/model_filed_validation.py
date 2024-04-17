from django.core.exceptions import ValidationError
import re



# Create your models here.

def phone_number_validation(number):
    ptn = "^[6-9]\d{9}$"
    if not re.match(ptn, str(number)):
        raise ValidationError("Incorrect Phone Number Format.")
    return number
