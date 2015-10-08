import unittest

import authentication_service
from mock import MagicMock
from pyramid import testing
from pyramid.httpexceptions import HTTPBadRequest
from v1.dao.user_dao import UserDao


class TestAuthenticationService(unittest.TestCase):
    def setUp(self):
        self.userdao = UserDao()
        authentication_service.userdao = self.userdao

    def test_authentication(self):
        self.userdao.find_by_username = MagicMock(return_value={"username": "test",
                                                                "password": "$pbkdf2-sha256$200000$zxljzJlTKoVwDkEo5by3Vg$5hMqFD5sd84K3iTjO/gWXNkFlHH3ZLnyy95GAICfYnI",
                                                                "roles": ["test"]})

        faulty_request = testing.DummyRequest()
        faulty_request.json = {
            "username": "test",
            "password": "asfasfasfasf"
        }
        with self.assertRaises(HTTPBadRequest):
            authentication_service.authenticate(faulty_request)

        faulty_request = testing.DummyRequest()
        faulty_request.json = {
            "username": "test",
            "password": "admin"
        }
        token = authentication_service.authenticate(faulty_request)

        self.assertIsNotNone(token)


if __name__ == '__main__':
    unittest.main()
