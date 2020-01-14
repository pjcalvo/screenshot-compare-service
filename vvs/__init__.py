from dynaconf import settings
import os
import json

app_settings = {
    'ENV': settings.ENV_FOR_DYNACONF,
}

# create google credentials variable
credentials = json.loads(os.environ['GOOGLE_CREDENTIALS'])
with open("credentials.json", 'w') as f:
    json.dump(credentials, f)