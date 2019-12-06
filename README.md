# IcingaHostManager
A web application for managing automated Host object configuration that integrates with Icinga2 through a shared host management database.

## Setup
### Create a virtual environment with python >= 3.6
``` python3.7 -m venv ihmvenv ```
### Activate virtual environment
``` source ihmvenv/bin/activate ```
### Install requirements
``` LDFLAGS=-L/usr/local/opt/openssl/lib pip install -r requirements.txt ```
#### (The LDFlags portion is needed to prevent the mysqlclient installation from failing. )
#### Django 3.0 fails to run unless you manually copy the six.py file into the Django utils directory: 
``` cp six.py <yourvenv>/lib/pythonX.Y/site-packages/django/utils/six.py ```
### Create a config.py file in this directory (same as manage.py) that contains the following variables that point to 
### the database where your Icinga Hosts are to be stored. 
```DBNAME=xxx```
```DBHOST=xxx```
```DBPASSWORD=xxx```
```DBUSER=xxx```
```DBPORT=xxx```

### If you want to add custom fields or edit the name/required/description of existing fields, you can find them in fields.json

### If you want to include API calls to Icinga to include things like host status on the front end: 
``` [api] ```
``` ICINGA_MASTER_URL = http[s]://youricingaurl[:optionalport] ```
``` ICINGA_API_USER = "<apiuser> # Configured in the /etc/icinga2/api-users.conf file on your Icinga server(s) ```
``` ICINGA_API_PASSWORD = "<apipassword>" # Same location as above ```


### Compress the static files (js,css,etc.)
``` python manage.py compress ```

# Customization
## Adding Fields
### Add to MODAL_FIELDS here
### Add to available_fields list in index with description
### Add a column to the edit hosts table in hostmanager.html
### Increment the TOTALNUMFIELDS variable in main.js
### Recompress
### Add an input field for this field to the add single host form with input name prefixed by 'host'