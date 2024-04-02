# utils.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


def custom_payload_handler(token):
    payload = TokenObtainPairSerializer.get_token_payload(token)
    try:
        user_type = token.user.user_profile.user_type
    except AttributeError:
        user_type = None
    payload['user_type'] = user_type
    payload['user_id'] = token.user.id  # bu qator qo'shildi
    return payload