import os
from flask import Flask, redirect, url_for, request, session, make_response, jsonify
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

from auth import AuthenticationManager, token_required, token, current_user
from route import route_bp
from bus import bus_bp
from driver import driver_bp
from customer import customer_bp
from model import db, User, Blacklist

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')


db.init_app(app)

app.register_blueprint(route_bp, url_prefix='/routes')
app.register_blueprint(bus_bp, url_prefix='/buses')
app.register_blueprint(driver_bp, url_prefix='/drivers')
app.register_blueprint(customer_bp, url_prefix='/customers')


auth_manager = AuthenticationManager(os.getenv('FLASK_SECRET_KEY'))



@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return 'Logged In Currently'


@app.route('/login', methods=['POST'])
def login():

    email = request.json.get('email')
    password = request.json.get('password')

    if email and password:
        if auth_manager.verify_credentials(email, password):
            user = User.get_by_email(email)
            token = auth_manager.generate_jwt_token(
                {
                    "id": user.id,
                    "role": user.role,                    

                }
            )

            return make_response(
                jsonify({"token": token}),
                200
            )
        else:
            return make_response(
                'Could Not Verify Account. Please Sign Up!',
                401)
    else:
        return make_response(
            'Could Not Verify',
            400
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

    new_blacklist = Blacklist(token=token)

    db.session.add(new_blacklist)
    db.session.commit()
    
    return jsonify({'message': 'Successfully Logged Out'})



@app.route('/delete', methods=['DELETE'])
@token_required
def delete():
    
    db.session.delete(current_user)
    db.session.commit()

    return ('', 204)
    
    




if __name__ == "__main__":
    app.run(debug=True)