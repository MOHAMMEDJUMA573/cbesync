
CONN_MAX_AGE = config("CONN_MAX_AGE", cast=int, default=30) # type:ignore
CONN_HEALTH_CHECKS=True,
DATABASE_URL = config("DATABASE_URL",cast=str) # type:ignore
if DATABASE_URL is not None:
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            #conn_max_age=30, disabled for asgi
            conn_health_checks=True,
        )
    }
