import datetime

from django.core.exceptions import ValidationError


def year_validator(year):
    if year > datetime.datetime.now().year:
        raise ValidationError(f'The {year} from the future')
