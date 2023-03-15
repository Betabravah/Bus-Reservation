import os
from flask import Blueprint, request, make_response, jsonify, abort, redirect, url_for
from auth import AuthenticationManager, token_required, token, current_user
from dotenv import load_dotenv
from uuid import uuid4

from model import User, UserRole, Route, Bus, db

load_dotenv()

driver_bp = Blueprint('driver_bp', __name__)

auth_manager = AuthenticationManager(os.getenv('FLASK_SECRET_KEY'))


class DriverManager:
    def modify(self, request_params: dict, driver: User):
        for param in request_params:
            if param == 'id':
                return make_response(
                    "Unprocessable Entity",
                    422
                )
            
            elif param == 'email':
                user = User.get_by_email(request_params['email'])
                if user:
                    return make_response(
                        "Email Already Exists",
                        400
                    )
                
            driver.__setattr__(param, request_params[param])

        db.session.commit()

        return make_response(
            "Updated successfully",
            200
        )
    
    def assign(self, driver: User, bus: Bus):
        

driver_manager = DriverManager()


@driver_bp.route('/', methods=['GET'])
def see_drivers():
    drivers = User.get_all_drivers()

    jsonList = []
    for driver in drivers:
        jsonList.append({
            "id": driver.id,
            "firstname": driver.firstname,
            "lastname": driver.lastname,
            "email": driver.email,
            "phonenumber": driver.phonenumber,
            "role": driver.role,
        })

    response = make_response(
        jsonify(jsonList),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response


@driver_bp.route('/', methods=['POST'])
def create():
    fname = request.json.get('firstname')
    lname = request.json.get('lastname')
    email = request.json.get('email')
    dob = request.json.get('dob')
    phone = request.json.get('phone')

    if not fname or not lname or not email:
        return make_response(
            "Please Send all required fields",
            400
        )

    new_driver = User(firstname=fname, lastname=lname, email=email,
                    dob=dob, phonenumber=phone, role=UserRole.DRIVER)
    
    db.session.add(new_driver)
    db.session.commit()

    return make_response(
        "Driver Created Successfully",
        201
    )


@driver_bp.route('/<id>', methods=['GET'])
def get(id):
    driver = User.get_by_id(id)

    if driver:
        return jsonify({
            "id": driver.id,
            "firstname": driver.firstname,
            "lastname": driver.lastname,
            "email": driver.email,
            "dob": driver.dob,
            "phonenumber": driver.phonenumber,
            "role": UserRole.DRIVER,
            }
        )
    
    return make_response(
        "Driver Not Found",
        404
    )


@driver_bp.route('/update/<id>', methods=['PATCH'])
def update(id):

    driver = User.get_by_id(id)
    request_params = request.get_json()

    if driver:
        return driver_manager.modify(request_params, driver) 

    else:
        return make_response(
            "Driver Not Found",
            404
        )



@driver_bp.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    driver = User.get_by_id(id)

    db.session.delete(driver)
    db.session.commit()
    return ('', 204)


@driver_bp.route('/assign', methods=['POST'])
def assign():
    driverId = request.json.get('driverId')
    busId = request.json.get('busId')

    driver = User.get_driver(driverId)
    bus = Bus.get(busId)

    if driver and bus:
        return driver_manager.assign(driver, bus)
    
    return make_response(
        "Not Found",
        404
    )


