#Basicly allauth ui settings adn stuff
AUTHENTICATION_BACKENDS = [   
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
    
]
ACCOUNT_SIGNUP_FIELDS=['email*', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS={"email","username"}
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE=True
ACCOUNT_EMAIL_VERIFICATION="mandatory"
# ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED=True
# ACCOUNT_EMAIL_VERIFICATION_BY_CODE_MAX_ATTEMPTS=3
# ACCOUNT_EMAIL_VERIFICATION_BY_CODE_TIMEOUT=600
# ACCOUNT_EMAIL_VERIFICATION_SUPPORTS_RESEND=False
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS=True
LOGIN_REDIRECT_URL="/"

ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION=True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE=True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=1
ACCOUNT_MAX_EMAIL_ADDRESSES=2
ACCOUNT_USERNAME_BLACKLIST=[
    "ADMIN","admin","Admin"
]

#Usermodels
ACCOUNT_PRESERVE_USERNAME_CASING=False
#user form for signup
ACCOUNT_FORMS = {
    'signup': 'schools.forms.SchoolSignupForm',
}