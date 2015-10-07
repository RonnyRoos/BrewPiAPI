""" Cornice services.
"""
import logging
from api.v1.dao.user_dao import UserDao

import colander
from cornice import Service
from pyramid.httpexceptions import HTTPBadRequest
from utils import auth_utils
from utils.auth_utils import hash_password, verify_password_hash

authentication = Service(name='authentication', path='/authentication', description="Authentication service")
logger = logging.getLogger(__name__)


class AuthenticationRequest(colander.MappingSchema):
    username = colander.SchemaNode(colander.String())
    password = colander.SchemaNode(colander.String())


@authentication.post()
def authenticate(request):
    """Registers a new token for the user"""
    authentitcationrequest = AuthenticationRequest().deserialize(request.json)
    userdao = UserDao()
    user = userdao.find_by_username(authentitcationrequest["username"])
    logger.debug("Creating new token for user {}".format(user["username"]))

    if verify_password_hash(authentitcationrequest["password"], user["password"]):
        token = auth_utils.create_token(user)
        logger.debug("Token created: {}".format(token))

        return {'token': token}

    raise HTTPBadRequest
