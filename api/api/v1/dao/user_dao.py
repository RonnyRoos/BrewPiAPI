from api.v1.domain.user import User
from config import USERS


class UserDao(object):
    def find_by_username(self, username):
        for user in USERS:
            if user["username"] == username:
                schema = User()
                deserializeduser = schema.deserialize(user)
                return deserializeduser

        return None
