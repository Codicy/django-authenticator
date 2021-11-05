from setuptools import setup

setup(
    name='jupyterhub-django-authenticator',
    version='0.1.0-alpha',
    description='Django Session Authenticator for JupyterHub',
    url='https://github.com/Codicy/django-authenticator',
    download_url='https://github.com/Codicy/django-authenticator/archive/refs/tags/v0.1.0-alpha.tar.gz',
    author='grahamdaley',
    author_email='gd@codicy.co',
    license='Apache 2.0',
    keywords=['jupyterhub', 'django', 'python'],
    tests_require = [
        'unittest',
    ],
    test_suite = 'unittest.collector',
    packages=['djangoauthenticator'],
    install_requires=[
        'jupyterhub',
    ]
)