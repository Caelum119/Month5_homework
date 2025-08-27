from datetime import date
from rest_framework.exceptions import ValidationError

def validate_age(user):
    """
    Raises a ValidationError if the user is under 18 years old.
    """
    if not user.birth_date:
        raise ValidationError("Дата рождения не указана.")

    today = date.today()
    age = today.year - user.birth_date.year - (
        (today.month, today.day) < (user.birth_date.month, user.birth_date.day)
    )

    if age < 18:
        raise ValidationError("Вам должно быть 18 лет, чтобы создать продукт.")
