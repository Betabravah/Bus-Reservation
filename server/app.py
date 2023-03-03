import os
from flask import Flask, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


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


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))




@app.route('/')
def home():
    return



if __name__ == "__main__":
    app.run(debug=True)