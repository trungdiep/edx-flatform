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
JWT_AUTH["JWT_SECRET_KEY"] = "Hw5D9P8CZqlfKPClE6lStvwa"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "CejtEfe2IX-i-DymXclJtU2fW0riQfK2lrHIqwfIvQFG6bw11vZhuGfc1plKYIB7Dvz4DoDuEynsFopYIlUl-ESg0e88hu79OpkDWLchU8ZmC6ltX4KRR_E0cU5h_TwrBPd7_w6L_txaSve87pbUxEwO2IqakKG8aIouPhRGyC0UXUWYIiLbZpqzIsfvrDKVM8qn0nhXpYAJgudnra409MBlVvJsc6ZcXe5ST9s42nXDOM_G8qo4XIrcj5JFYRWuVZHNVMWq6zbDQxgubGAJtMn7QZlFLYP24Dltn4KyermJWJMB28H1Ii-wVMCYK42uEjaoKsai4QKYPcjz02aBOQ",
        "n": "kUDL_gp0YdW-haOnc7TLsFIGx6HY-KfJdapW0OtrAuC_odK3QOWED2Csl49-P760Wbg727Mj3HHWM7J1Ydmgx9pjgyF6O_JTT39nHUx6-kXtI1bB1Qbmy0-BfxTB5lSNFVAyh5ThJhR6MyiozjfCACITIPYk21wjr3n0TmlP4cR55QBF2Vm0ouuWcHbrMABn-yIK5zHOt5KqnxuwTsJXDMqZhyQssZKKKTwx23tC4nsA0eGFzKIh8_DBE2H2YLussBxKoW-S5lVw1DwVUCnEyF1gzIscOvF4vyFnvNIFqgQ16ebcRKmGGUKvv8KtuiKg_kB2RBl8BAurPi7CTVWZtQ",
        "p": "uphlmxIK7fb-Mh9KjeH7QDHt0sj88mpaOIVudgfWZpnk0W_kfwrYAXvxcaf4Wdy39MpwXOu65wJAFO5ekAvhBWJApMp4a8Z6tOddEJIAFtPtT0OecV6JN3fsoUe-dZmLXsGBVGRVTZGL1GniicN-kJ0Qo2vX5BB6l0Je7H_vgAk",
        "q": "x0fMEaqUqufAsNp3RUOzHXy_nRCrr5vrvPMp0sxyNT4hrdk6Errvm6eKmr8YqYRCbaE2vrtOUNfiVcBIhfVoOGqFPesP2OgxRqIHOX_xiWEGXATDzOWWpt2jxaxwC0CUUZOHTPIwTLuY4gmhgh_mxdq9YNrCEG9--J9vRNAzH00",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "kUDL_gp0YdW-haOnc7TLsFIGx6HY-KfJdapW0OtrAuC_odK3QOWED2Csl49-P760Wbg727Mj3HHWM7J1Ydmgx9pjgyF6O_JTT39nHUx6-kXtI1bB1Qbmy0-BfxTB5lSNFVAyh5ThJhR6MyiozjfCACITIPYk21wjr3n0TmlP4cR55QBF2Vm0ouuWcHbrMABn-yIK5zHOt5KqnxuwTsJXDMqZhyQssZKKKTwx23tC4nsA0eGFzKIh8_DBE2H2YLussBxKoW-S5lVw1DwVUCnEyF1gzIscOvF4vyFnvNIFqgQ16ebcRKmGGUKvv8KtuiKg_kB2RBl8BAurPi7CTVWZtQ",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://local.overhang.io/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "Hw5D9P8CZqlfKPClE6lStvwa"
    }
]


######## End of settings common to LMS and CMS

######## Common CMS settings

STUDIO_NAME = u"newwave - Studio"
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

