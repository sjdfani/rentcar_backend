from rest_framework_simplejwt.tokens import RefreshToken
import string
import random


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
