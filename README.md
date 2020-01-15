api Visual Validation Service

# Information
This service exposes several endpoints for comparing the websites rendering by taking screenshots using selenium and comparing target tests against baselines.

```bash
curl --request POST \
  --url http://localhost:5000/api/crosssite \
  --header 'content-type: application/json' \
  --data '{
	"browser":"chrome",
	"urls":{
		"base":"https://www.google.com",
		"targets":[
			"https://www.google.com",
			"https://www.google.com?q=hola"]
	}
}'
```

```bash 
curl --request POST \
  --url http://localhost:5000/api/crossbrowser \
  --header 'content-type: application/json' \
  --data '{
	"url":"https://www.google.com",
	"browsers":{
		"base":"chrome",
		"targets":["firefox", "chrome"]
	}
}'
```

# Tech Stack
    * Python3
    * Flask
    * Pillow
    * Selenium Webdriver

# Running
```bash
python 3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
FLASK_APP=api/run.py flask run #dev server
or
gunicorn api.run:app  #production server
```

**To use configuration:**
```bash
export FLASK_ENV=development
export FLASK_ENV=production
```

**Code Style Check:**
Using Pep8 for coding standards and code styling. For custom config setup .pycodestyle
```bash
pycodestyle api/* --.pycodestyle
```

**Codecoverage:**
Suggested codecoverage above 90%. `.coveragerc` stores the configuration for the pytest-cov execution
```bash
pytest --cov-config=.coveragerc --cov=api/
```

**Secrets**
Secrets are not committed but can be readed as a setting file, for DB passwords and so use the .secrets file

**Deployment to heroku**
Once the master build has finished testing,  a manual triggered will be waiting to deploy to heroku.
- This will allow us to deploy on demand and skip configuration, miscelaneus or undesired deployments to staging.
- To deploy live go to Heroku pipelines and promote the latest build on staging

# Contributors
    * Pablo Calvo

