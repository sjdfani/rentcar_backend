from rest_framework_simplejwt.tokens import RefreshToken
import string
import random

user_messages = {
    "username_exists": "This username is taken.",
    "email_exists": "This email is taken.",
    "password": "Your email or password is incorrect.",
    "email_not_exists": "This email is not exists.",
    "role": "You should choose between admin or superuser.",
    "wrong_password": "Your input password is incorrect.",
    "equal_passwords": "Your new_password and confirm password isn't equal.",
    "successful_change_password": "Your password changed.",
    "unique_id_not_found": "your unique id not found or your code was expired.",
    "correct_code": "Your input code is correct.",
    "invalid_code": "Your input code is invalid.",
    "expire_code": "Your code was expired.",
    "verify_email": "Your email verified.",
    "wrong_code": "Your code was expired.",
    "verified_user": "Your email was verified.",
    "id_token_invalid": "Your id_token is invalid.",
}


def get_user_messages(title: str):
    return user_messages.get(title, "")


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def str_generator(size=10, generate_number=False):
    if generate_number:
        chars = string.digits
    else:
        chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(size))
