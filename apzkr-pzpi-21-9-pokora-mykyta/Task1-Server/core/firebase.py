import firebase_admin
from firebase_admin import credentials
import pyrebase
from core.config import settings

cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)

firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
pyrebase_auth = firebase.auth()
