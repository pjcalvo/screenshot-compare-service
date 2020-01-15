from dynaconf import settings
import os
import json

app_settings = {
    'ENV': settings.ENV_FOR_DYNACONF,
}

# create google credentials variable
try:
    credentials = json.loads(os.environ['GOOGLE_CREDENTIALS'])
    with open("credentials.json", 'w') as f:
        json.dump(credentials, f)   
except KeyError as ex:
    print('GOOGLE_CREDENTIALS not found on ENV. Images will not be update') 