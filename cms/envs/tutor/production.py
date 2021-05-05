# -*- coding: utf-8 -*-
import os
from cms.envs.production import *

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "host": "mongodb",
    "port": 27017,
    
    "user": None,
    "password": None,
    
    "db": "openedx",
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/"
for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

LOCALE_PATHS.append("/openedx/locale/contrib/locale")
LOCALE_PATHS.append("/openedx/locale/user/locale")

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "http://local.overhang.io/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "Byz64ntHnPIkELWwA3fE7jdC"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "I8n2RhvFlVu7jxsWDV9e4RjNDNSZ__CWzIHohdC7aFC76pygglMD9qZKeIpXg_K3r_o-IlJsXYGMgJg4Pi9Uolw1DEiAhmoeBP2r-G9ksOjb0yUEm0HU7xuoyaD7OwjhZC7gB3VV2ROKUMpO2t6dewE0LMwcjFjGsiE1XVsumKc1nrcKEuGVLtCkgegLnG73luka6oqqr3kGuVtDL0TWO1S6BtJrjNmHHAHmA9LIFiUxyPea5wDiVj9MG1p1J1G0GaLTWyShW80Ocfo1qIrNAnoL9bzOtMBBVdvzaCGzfQQgWTiMWhmdTcpBoN54wRsJ9z3tETK6yO2LqCkKbNPWOw",
        "n": "7NXUCCtrSp9is7I5HQBHJlbiQCzYKsUsPms5atrzWRFjxl6p7tl6lRSQ_DVNkZpgW938KbxEMGNQVLOSaKdEYHCwM9ek4OgjpjDn-ceZimYzrFI_Gwlz8jY0HrQDDPdj5Za4fwH8QzFYA1MpUy7Im5RktaAowCW3J2EQhPvS903dZJifovDLzm3ckRrJvqFVi7bHX1lSL5s3CybHsVEsCPxART8HxHBRThZ_1UoK1KezREOBwRSXNY3RzvL-b6fj28vVpgr9azJFrDGTNsluGUdz6CSVjPWrRilbLRHOcIl9d6ddTKY_KfOISGVNDb42wYUHM7OobWp38ljO5nMNxQ",
        "p": "7URcTUnM3gxKLd12ymDFl_OEZgQyWlI_gH13DGP9fnlBTYKUAHERbAI6klFKI0gomYwkajM-DAlYRjbNvxrXbDXHmnEI9PBf_6zEGRuZ2GHwhGw3jgx-JPDh35vimAqWHXjgTU5QKC9nKno20rlGgV2c9FpqzX1FxA5Hoy70Fps",
        "q": "_4i9puQQbHZJ58n5IdmwKGhYLToTYaMTQIPWkcLdHpV0_Y0in9fmFt_pXnI1IX4DduBfM7bXPuaHTEWvIM8Srs1tCb61UykdDKz9YJllmI1sWne0nUWicg0gQx9rEFROM1TR9MUrzXPRxjiTRksDFkD5S1brDEsjR16dO9mpgx8",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "7NXUCCtrSp9is7I5HQBHJlbiQCzYKsUsPms5atrzWRFjxl6p7tl6lRSQ_DVNkZpgW938KbxEMGNQVLOSaKdEYHCwM9ek4OgjpjDn-ceZimYzrFI_Gwlz8jY0HrQDDPdj5Za4fwH8QzFYA1MpUy7Im5RktaAowCW3J2EQhPvS903dZJifovDLzm3ckRrJvqFVi7bHX1lSL5s3CybHsVEsCPxART8HxHBRThZ_1UoK1KezREOBwRSXNY3RzvL-b6fj28vVpgr9azJFrDGTNsluGUdz6CSVjPWrRilbLRHOcIl9d6ddTKY_KfOISGVNDb42wYUHM7OobWp38ljO5nMNxQ",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://local.overhang.io/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "Byz64ntHnPIkELWwA3fE7jdC"
    }
]


######## End of settings common to LMS and CMS

######## Common CMS settings

STUDIO_NAME = u"NewWave - Studio"
MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 100

FRONTEND_LOGIN_URL = LMS_ROOT_URL + '/login'
FRONTEND_LOGOUT_URL = LMS_ROOT_URL + '/logout'
FRONTEND_REGISTER_URL = LMS_ROOT_URL + '/register'

# Create folders if necessary
for folder in [LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE]:
    if not os.path.exists(folder):
        os.makedirs(folder)



######## End of common CMS settings

ALLOWED_HOSTS = [
    ENV_TOKENS.get("CMS_BASE"),
    "cms",
]

