import os.path
from pathlib import Path

from split_settings.tools import include, optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

#Namespace current env variable
LOCAL_SETTINGS_PATH = os.getenv(f'LOCAL_SETTINGS_PATH')

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = 'local/settings.dev.py'

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

include(
    'base.py',
    'custom.py',
    optional(LOCAL_SETTINGS_PATH),
    'docker.py',
    'logging.py',
    'templates.py',
    'database.py',
    'staticf.py'
)