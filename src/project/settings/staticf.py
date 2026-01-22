
# Static files (CSS, JavaScript, Images) and caching for faster send and retrieval
# https://docs.djangoproject.com/en/6.0/howto/static-files/
CLOUDFLARE_R2_BUCKET=config("CLOUDFLARE_R2_BUCKET", cast=str) # type:ignore
CLOUDFLARE_R2_ACCESS_KEY=config("CLOUDFLARE_R2_ACCESS_KEY", cast=str) # type:ignore
CLOUDFLARE_R2_SECRET_KEY=config("CLOUDFLARE_R2_SECRET_KEY", cast=str) # type:ignore
CLOUDFLARE_R2_BUCKET_ENDPOINT=config("CLOUDFLARE_R2_BUCKET_ENDPOINT", cast=str) # type:ignore


CLOUD_FLARE_R2_CONFIG_OPTIONS = {
    "bucket_name": CLOUDFLARE_R2_BUCKET,
    "access_key": CLOUDFLARE_R2_ACCESS_KEY,
    "secret_key": CLOUDFLARE_R2_SECRET_KEY,
    "endpoint_url": CLOUDFLARE_R2_BUCKET_ENDPOINT,
    "default_acl": "private", #public read is also an option
    "signature_version": "s3v4",
}

# Source - https://stackoverflow.com/a
STATIC_URL = 'static/'

print(f"{BASE_DIR2}/staticfilesdev/")

if not DEBUG: # type:ignore
    STATICFILES_DIRS = [
        f"{BASE_DIR2}/staticfilesdev/",
    ]
    STATIC_ROOT=f"{BASE_DIR2}/staticfiles"  # type:ignore
if DEBUG:
    STATIC_ROOT=f"{BASE_DIR2}/staticfilesdev"
STORAGES = {
    "default": {
        "BACKEND": "helpers.cloudr2.storages.MediaFileStorage", #django-storages s[3]
        "OPTIONS": CLOUD_FLARE_R2_CONFIG_OPTIONS,
    }, #default user file fields upload
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

