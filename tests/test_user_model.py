import unittest
from app.models import User, Permission, AnonymousUser, Role
from flask import config

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password = "cat" )
        self.assertTrue(u.password_hash is not None)

    def test_password_getter(self):
        u = User(password = "cat")
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password = "cat")
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password("dog"))
    #verify 核实 查证
    def test_password_salts_are_random(self):
        u = User(password = "cat")
        u2 = User(password = "dog")
        self.assertTrue(u.password_hash != u2.password_hash)
    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = User(email = "john@example.com", password = "cat")
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMITS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))



