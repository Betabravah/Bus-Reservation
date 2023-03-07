import os
import jwt
from datetime import datetime, timedelta
from flask import Flask, redirect, url_for, request, session, make_response, jsonify
from werkzeug.security import generate_password_hash

from auth import AuthenticationManager, token_required
from route import route_bp
from bus import bus_bp
from driver import driver_bp
from customer import customer_bp
from model import db, User, UserRole

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost:3306/brs"


db.init_app(app)

app.register_blueprint(route_bp, url_prefix='/routes')
app.register_blueprint(bus_bp, url_prefix='/buses')
app.register_blueprint(driver_bp, url_prefix='/drivers')
app.register_blueprint(customer_bp, url_prefix='/customers')



print(os.getenv('FLASK_SECRET_KEY'))
auth_manager = AuthenticationManager(os.getenv('FLASK_SECRET_KEY'))



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


@app.route('/register', methods=['POST'])
def register():
    fname = request.json.get('firstname')
    lname = request.json.get('lastname')
    email = request.json.get('email')
    dob = request.json.get('dob')
    phone = request.json.get('phone')
    role = request.json.get('role')
    password = request.json.get('password')
    confirm = request.json.get('confirm')


    if password != confirm:
        return make_response(
            "Passwords Do Not Match!",
            400)
    
    if User.get_by_email(email):
        return make_response(
            "User Already exists",
            400
        )
    
    new_user = User(firstname=fname, lastname=lname, email=email,
                    dob=dob, phonenumber=phone, role=role,
                    password=generate_password_hash(password))
    
    db.session.add(new_user)
    db.session.commit()
    return make_response (
        "User Created successfully",
        201
    )
        


@app.route('/logout')
@token_required
def logout():
    response = jsonify({'message': 'Successfully Logged Out'})
    return response



app.route('/delete', methods=['POST'])
@token_required
def delete():
    id = request.json.get('id')
    user = db.session.query(User).filter(User.id==id).first()
    
    if user:
        db.session.delete(user)
        db.session.commit()

        return ('', 204)
    
    return make_response(
        "Not Found!",
        404
    )





if __name__ == "__main__":
    app.run(debug=True)