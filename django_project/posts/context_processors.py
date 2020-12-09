import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(BASE_DIR, 'secrets.json'), 'rb') as secret_file:
    secrets = json.load(secret_file)


def kakao_login_key(request):
    return {'javascript_sdk_key': str(secrets["kakao"]["javascript_key"])}
