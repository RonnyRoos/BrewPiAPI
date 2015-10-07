import logging

from cornice import Service
from utils.auth_utils import valid_token, get_authenticated_user

userservice = Service(name='userservice_v1', path='/api/v1/user', description="User service")
logger = logging.getLogger(__name__)

@userservice.get(validators=valid_token)
def get_info(request):
    """
    Returns the current authenticated user.
    """
    user = get_authenticated_user(request)
    user["password"] = user["password"]
    return user

