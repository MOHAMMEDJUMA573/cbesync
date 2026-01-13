#sending email
ACCOUNT_EMAIL_SUBJECT_PREFIX="CbeSync "
ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS=False
ACCOUNT_EMAIL_NOTIFICATIONS=True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1  # Link expires after 1 day
#django axes for brute force protection

EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"