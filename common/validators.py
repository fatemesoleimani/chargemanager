from django.core.validators import RegexValidator

PHONE_REGEX = RegexValidator(regex=r'^(0)?9\d{9}$',
                             message="not valid phone number")
