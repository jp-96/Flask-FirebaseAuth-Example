# coding: utf-8

from flask import Flask, request, redirect, Response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_firebaseauth import FirebaseAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

app.config['FIREBASE_API_KEY'] = '<The API key>'
app.config['FIREBASE_PROJECT_ID'] = '<The project identifier, eg. `foobar`>'
app.config['FIREBASE_AUTH_SIGN_IN_OPTIONS'] = 'email,facebook,github,google,twitter' #Comma-separated list of enabled providers.

login_manager = LoginManager()
login_manager.init_app(app)
auth = FirebaseAuth(app)
app.register_blueprint(auth.blueprint, url_prefix='/auth')

class User(UserMixin):
    # user database
    users = {
        'user01@your.domain': {'name': 'debug01'},
        'user02@your.domain': {'name': 'debug02'},
        'user03@your.domain': {'name': 'debug03'},
        'user04@your.domain': {'name': 'debug04'},
    }

    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    @classmethod
    def get(self, id):
        user = self.users.get(id)
        if user is not None:
            return User(id, user['name'])

@auth.production_loader
def production_loader(token):
    user = User.get(token['email'])
    if user is not None:
        login_user(user, True)


@auth.development_loader
def development_loader(email):
    user = User.get(email)
    if user is not None:
        login_user(user, True)

@auth.unloader
def sign_out():
    logout_user()

@login_manager.user_loader
def user_loader(user_id):
    return User.get(user_id)

@login_manager.request_loader
def request_loader(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')
    return User.get(token)

@login_manager.unauthorized_handler
def authentication_required():
    return redirect(auth.url_for('widget', mode='select', next=request.url))

@app.route('/')
def homepage():
    return Response("home: <a href='/login/'>Login</a> <a href='/protected/'>Protected</a> <a href='/logout/'>Logout</a>")

@app.route('/login/')
@login_required
def login():
    return redirect("/")

@app.route('/logout/')
def logout():
    return auth.sign_out()

@app.route('/protected/')
@login_required
def protected():
    return Response("<h1>Protected Page</h1><a href='/logout/'>Logout</a><br />" + current_user.name)

if __name__ == '__main__':
    auth.debug = True
    app.run(debug=True)