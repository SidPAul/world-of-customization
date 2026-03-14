import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings
import os

def initialize_firebase():
    if not firebase_admin._apps:
        service_account_path = settings.FIREBASE_SERVICE_ACCOUNT_PATH
        if service_account_path and os.path.exists(service_account_path):
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
        else:
            # Fallback for environments where service account is not provided
            # (Note: Token verification will fail if not properly configured)
            firebase_admin.initialize_app()

def verify_token(token):
    initialize_firebase()
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Firebase token verification failed: {e}")
        return None
