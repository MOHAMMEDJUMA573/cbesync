#sending email
ACCOUNT_EMAIL_SUBJECT_PREFIX="CbeSync "
ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS=False
ACCOUNT_EMAIL_NOTIFICATIONS=True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1  # Link expires after 1 day
#django axes for brute force protection

if DEBUG: # type:ignore
    EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST="smtp.gmail.com"
    EMAIL_HOST_USER=config("APP_EMAIL", default="") # type:ignore
    EMAIL_HOST_PASSWORD=config("APP_EMAIL_PASSWORD", default="") # type:ignore
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_USE_SSL=False
    DEFAULT_FROM_EMAIL="cbesync@cbesync.com"
    ACCOUNT_EMAIL_SUBJECT_PREFIX=""
    
    #sendgrid config
    # EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
    # SENDGRID_API_KEY = config("SENDGRID_API_KEY", default="") # type:ignore
    # DEFAULT_FROM_EMAIL = "cbesync@cbesync.com"
    SERVER_EMAIL = DEFAULT_FROM_EMAIL