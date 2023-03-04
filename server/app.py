import os
import jwt
from functools import wraps
from datetime import datetime, timedelta
from flask import Flask, redirect, url_for, request, session, make_response, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


from auth import AuthentcationManager
from route import route_bp
from bus import bus_bp
from driver import driver_bp
from customer import customer_bp
from model import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')


app.register_blueprint(route_bp, url_prefix='/routes')
app.register_blueprint(bus_bp, url_prefix='/buses')
app.register_blueprint(driver_bp, url_prefix='/drivers')
app.register_blueprint(customer_bp, url_prefix='/customers')


login_manager = LoginManager()
login_manager.init_app(app)

auth_manager = AuthentcationManager(os.getenv('FLASK_SECRET_KEY'))


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


def token_required(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            token = None

            if 'access-token' in request.headers:
                token = request.headers['access-token']

            if not token:
                return make_response(
                    jsonify({'message': "A Valid Token is Missing!"}),
                    401
                )
            try:
                data = auth_manager.verify_token(token)
                current_user = User.get(data['username']).first()

            except:
                return make_response(
                    jsonify({'message': 'Invalid Token!'}),
                    401
                )
            return func(current_user, *args, **kwargs)
        return decorator



@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return 'Logged In Currently'


@token_required
@app.route('/login', methods=['POST'])
def login():

    auth = request.get_json()
    username = auth.get('username')
    password = auth.get('password')

    if username and password:
        if auth_manager.verify_credentials(username, password):
            user = User.get(username)
            token = jwt.encode({
                'user': auth.get('username'),
                'role': user.role,
                'expiration': datetime.utcnow() + timedelta(seconds=120)
            })

            return make_response(
                jsonify({'token': token}),
                201
            )
        else:
            return make_response(
                'Could Not Verify Account. Please Sign Up!',
                401)
    else:
        return make_response(
            'Could Not Verify',
            401
        )


if __name__ == "__main__":
    app.run(debug=True)