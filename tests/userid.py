import unittest

from djangoauthenticator.djangoauthenticator import DjangoSessionLoginHandler


class TestUserIdFromSession(unittest.TestCase):

    def test_user_id_from_session(self):
        session_data = "NjkzNmU1NGYxNjhhNjI1NDI2NGZiYjdiMDIyMzk5MDc3MzU4ZGU4Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2NDk1YzcwOWM1MGRjNzNjYjgwOWZlNWY4OWY4OWNiNjk2MTllOGJkIn0="
        user_id = DjangoSessionLoginHandler.user_id_from_session(session_data)
        self.assertEqual(user_id, 1)
