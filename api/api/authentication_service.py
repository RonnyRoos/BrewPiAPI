""" Cornice services.
"""
import logging
from api.v1.dao.user_dao import UserDao

import colander
from cornice import Service
from cornice.tests.support import CatchErrors
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPBadRequest
from utils import auth_utils
from utils.auth_utils import hash_password, verify_password_hash

authentication = Service(name='authentication', path='/authentication', description="Authentication service")
logger = logging.getLogger(__name__)
userdao = UserDao()

class AuthenticationRequest(colander.MappingSchema):
    username = colander.SchemaNode(colander.String())
    password = colander.SchemaNode(colander.String())



@authentication.post()
def authenticate(request):
    """Registers a new token for the user"""
    authentitcationrequest = AuthenticationRequest().deserialize(request.json)
    user = userdao.find_by_username(authentitcationrequest["username"])
    if user is None:
        raise HTTPBadRequest

    logger.debug("Creating new token for user {}".format(user["username"]))

    if verify_password_hash(authentitcationrequest["password"], user["password"]):
        token = auth_utils.create_token(user)
        logger.debug("Token created: {}".format(token))

        return {'token': token}

    raise HTTPBadRequest


def includeme(config):
    config.include("cornice")
    config.scan("api.authentication_service")


def main(global_config, **settings):
    config = Configurator(settings={})
    config.include(includeme)
    return CatchErrors(config.make_wsgi_app())
