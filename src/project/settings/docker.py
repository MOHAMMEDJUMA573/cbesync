import os


if IN_DOCKER or os.path.isfile('/.dockerenv'): # type:ignore
    assert MIDDLEWARE[:1] == [  # type:ignore
        'django.middleware.security.SecurityMiddleware',
    ]
    