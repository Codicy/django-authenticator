from setuptools import setup

setup(
    name='jupyterhub-django-authenticator',
    version='0.1-dev',
    description='Django Session Authenticator for JupyterHub',
    url='https://github.com/Codicy/django-authenticator',
    author='grahamdaley',
    author_email='gd@codicy.co',
    license='Apache 2.0',
    tests_require = [
        'unittest',
    ],
    test_suite = 'unittest.collector',
    packages=['djangoauthenticator'],
    install_requires=[
        'jupyterhub',
    ]
)