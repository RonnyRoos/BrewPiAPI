import datetime
import logging
from api.v1.dao.user_dao import UserDao

from config import JWT_SECRET

import jwt
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from pyramid.httpexceptions import HTTPBadRequest

logger = logging.getLogger(__name__)


#
# Helpers
#
def create_token(user):
    return jwt.encode({
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=72),
        "user": user["username"],
        "roles": user["roles"]
    }, JWT_SECRET, algorithm='HS256')


def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET)
    except Exception:
        raise TokenException()


def valid_token(request):
    header = 'Authorization'
    htoken = request.headers.get(header)
    if htoken is None:
        raise HTTPBadRequest
    try:
        decode_token(htoken)
    except TokenException:
        raise HTTPBadRequest

def get_authenticated_user(request):
    header = 'Authorization'
    htoken = request.headers.get(header)
    token = decode_token(htoken)
    return UserDao().find_by_username(token["user"])

def hash_password(password):
    return pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)

def verify_password_hash(password, password_hash):
    return pbkdf2_sha256.verify(password, password_hash)

class TokenException(Exception):
    pass
