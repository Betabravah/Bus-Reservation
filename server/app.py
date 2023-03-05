import os
import jwt
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

print(os.getenv('FLASK_SECRET_KEY'))
auth_manager = AuthentcationManager(os.getenv('FLASK_SECRET_KEY'))



@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return 'Logged In Currently'


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