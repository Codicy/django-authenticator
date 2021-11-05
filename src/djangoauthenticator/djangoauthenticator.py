import base64
import json
import logging

from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from jupyterhub.auth import LocalAuthenticator
from jupyterhub.utils import url_path_join
from MySQLdb import connect, Error
from tornado import gen, httputil, web
from traitlets import Unicode
from traitlets.config import application
from traitlets.traitlets import Any

class DjangoSessionLoginHandler(BaseHandler):

    def __init__(self, application: "application", request: httputil.HTTPServerRequest, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self.db_connection = None

    def get(self):
        session_cookie_name = self.authenticator.django_session_cookie_name
        session_id = self.get_cookie(session_cookie_name, "")

        username = self.retrieve_username(session_id)
        if not username:
           raise web.HTTPError(401)

        user = self.user_from_username(username)
        self.set_login_cookie(user)

        _url = url_path_join(self.hub.server.base_url, 'home')
        next_url = self.get_argument('next', default=False)
        if next_url:
             _url = next_url

        self.redirect(_url)

    def get_db_connection(self):
        if (self.db_connection is None):
            try:
                self.db_connection = connect(user=self.authenticator.mysql_username,
                    password=self.authenticator.mysql_password,
                    host=self.authenticator.mysql_hostname)
            except Error as err:
                logging.error(err)
        return self.db_connection
    
    def get_session_data(self, session_key):
        db_connection = self.get_db_connection()
        try:
            db_cursor = db_connection.cursor()
            db_cursor.execute("SELECT session_data from {0}.django_session WHERE session_key=%s AND expire_date > now();".format(self.authenticator.mysql_db), (session_key))
            result = db_cursor.fetchone()
        except Error as err:
            logging.error(err)
        if result and len(result) == 0:
            logging.info("Session with id='{0}' not found".format(session_key))
        return next(iter(result or []), None)

    def user_id_from_session(self, session_data):
        decoded_session_data = json.loads(base64.b64decode(session_data)[41:])
        return int(decoded_session_data[u'_auth_user_id'])
    
    def retrieve_user(self, user_id):
        db_connection = self.get_db_connection()
        try:
            db_cursor = db_connection.cursor()
            db_cursor.execute("SELECT username from {0}.users WHERE id=%s;".format(self.authenticator.mysql_db), (user_id))
            result = db_cursor.fetchone()
        except Error as err:
            logging.error(err)
        if result and len(result) == 0:
            logging.info("User with id={0} not found".format(user_id))
        return next(iter(result or []), None)
    
    def retrieve_username(self, session_key):
        session_data = self.get_session_data(session_key)
        user_id = self.user_id_from_session(session_data)
        if user_id:
            user = self.retrieve_user(user_id)
            if user:
                return user
                
        return None


class DjangoSessionAuthenticator(Authenticator):
    """
    Accept the authenticated Django session token from cookie.
    """
    django_session_cookie_name = Unicode(
        default_value='sessionid',
        config=True,
        help="""
        The name of the session cookie set by Django upon successful user login.
        """
    )
    mysql_hostname = Unicode(
        config=True,
        help="""
        The hostname of the MySQL instance holding the django_sessions table
        """
    )
    mysql_username = Unicode(
        config=True,
        help="""
        The login ID of the MySQL instance holding the django_sessions table
        """
    )
    mysql_password = Unicode(
        config=True,
        help="""
        The password of the MySQL instance holding the django_sessions table
        """
    )
    mysql_db = Unicode(
        config=True,
        help="""
        The database of the MySQL instance holding the django_sessions table
        """
    )

    def get_handlers(self, app):
        return [
            (r'/login', DjangoSessionLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()


class DjangoSessionLocalAuthenticator(DjangoSessionAuthenticator, LocalAuthenticator):
    """
    A version of DjangoSessionAuthenticator that mixes in local system user creation
    """
    pass