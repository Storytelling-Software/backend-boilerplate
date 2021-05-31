import jwt
import time
from jwt.exceptions import (
    InvalidTokenError,
    DecodeError,
    InvalidSignatureError,
    ExpiredSignatureError,
    InvalidIssuedAtError,
    MissingRequiredClaimError
)


class TokensService:
    def __init__(self, jwt_secret, access_token_ttl, refresh_token_ttl) -> None:
        self.jwt_secret = jwt_secret
        self.access_token_ttl = access_token_ttl
        self.refresh_token_ttl = refresh_token_ttl

    def encode(self, token_type, data) -> str:
        iat = time.time()
        if token_type == 'access':
            exp = iat + 60 * self.access_token_ttl
        elif token_type == 'refresh':
            exp = iat + 3600 * self.refresh_token_ttl
        token_data = {
            'iat': iat,
            'exp': exp,
            'purpose': token_type
        }
        payload = {**data, **token_data}
        token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        return token.decode('utf-8')

    def decode(self, token) -> dict:
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'], options={
                'require_exp': True,
                'require_iat': True,
                'verify_exp': True,
                'verify_iat': True
            })
        except (InvalidTokenError, DecodeError,
                InvalidSignatureError,
                ExpiredSignatureError,
                InvalidIssuedAtError,
                MissingRequiredClaimError):
            payload = None
        return payload
