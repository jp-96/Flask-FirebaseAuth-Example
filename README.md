# Flask-FirebaseAuth Example

## Preparation

### virtualenv

```
py -3 -m virtualenv --python "C:\Python37\python.exe" venv
venv\Scripts\activate.bat
```

### Install packages

```
pip install git+https://github.com/jp-96/Flask-FirebaseAuth.git
pip install flask-login
```

## Settings for flask-login and Firebase Authentication

### flask-login

```
app.config['SECRET_KEY'] = "secret"
```

### Firebase

```
app.config['FIREBASE_API_KEY'] = '<The API key>'
app.config['FIREBASE_PROJECT_ID'] = '<The project identifier, eg. `foobar`>'
app.config['FIREBASE_AUTH_SIGN_IN_OPTIONS'] = 'email,facebook,github,google,twitter' #Comma-separated list of enabled providers.
```

## Run

```
python main.py
```

## Deploy

```
gcloud app deploy
```
