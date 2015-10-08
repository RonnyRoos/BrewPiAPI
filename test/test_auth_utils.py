from unittest import TestCase
from pyramid import testing
from pyramid.httpexceptions import HTTPBadRequest

from utils import auth_utils
from utils.auth_utils import TokenException


class TestAuthUtils(TestCase):
    def test_create_token(self):
        with self.assertRaises(TokenException):
            auth_utils.create_token(None)

        bad_user = {
            "username": None,
            "roles": ["cool"]
        }
        with self.assertRaises(TokenException):
            auth_utils.create_token(bad_user)

        bad_user = {
            "username": "stuff",
            "roles": []
        }
        with self.assertRaises(TokenException):
            auth_utils.create_token(bad_user)

        bad_user = {
            "username": "stuff",
            "roles": None
        }
        with self.assertRaises(TokenException):
            auth_utils.create_token(bad_user)

        bad_user = {
            "username": "stuff",
        }
        with self.assertRaises(TokenException):
            auth_utils.create_token(bad_user)
        bad_user = {
            "roles": ["role"]
        }
        with self.assertRaises(TokenException):
            auth_utils.create_token(bad_user)

        good_user = {
            "username": "user",
            "roles": ["role"]
        }
        token = auth_utils.create_token(good_user)
        self.assertIsNotNone(token)
        try:
            tokenuser = auth_utils.decode_token(token)
            self.assertEqual(good_user["username"], tokenuser["user"])
        except TokenException:
            self.fail()

    def test_decode_token(self):
        # Check invalid tokens
        with self.assertRaises(TokenException):
            auth_utils.decode_token(None)
        with self.assertRaises(TokenException):
            auth_utils.decode_token("asfafsasf1241243124")

        good_user = {
            "username": "user",
            "roles": ["role"]
        }
        token = auth_utils.create_token(good_user)
        try:
            auth_utils.decode_token(token)
        except Exception:
            self.fail("Should not be here")

        # test modified token not acceptable
        tokenlist = list(token)
        if tokenlist[0] != '?':
            tokenlist[0] = '?'
        else:
            tokenlist[0] = 'a'
        token = "".join(tokenlist)

        with self.assertRaises(TokenException):
            auth_utils.decode_token(token)

    def test_valid_token(self):
        request = testing.DummyRequest()
        with self.assertRaises(HTTPBadRequest):
            auth_utils.valid_token(request)

        headername = "Authorization"
        request.headers[headername] = "asfasfasfasf"
        with self.assertRaises(HTTPBadRequest):
            auth_utils.valid_token(request)

        good_user = {
            "username": "user",
            "roles": ["role"]
        }
        token = auth_utils.create_token(good_user)
        request.headers[headername] = token
        auth_utils.valid_token(request)

    def test_get_authenticated_user(self):
        headername = "Authorization"
        request = testing.DummyRequest()
        good_user = {
            "username": "user",
            "roles": ["role"]
        }
        token = auth_utils.create_token(good_user)
        request.headers[headername] = token
        self.assertIsNone(auth_utils.get_authenticated_user(request)) # with current impl. we don't have the user "user"