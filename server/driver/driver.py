from flask import Blueprint, request, make_response, jsonify, abort, redirect, url_for
from auth import AuthenticationManager, token_required, token, current_user
from uuid import uuid4


from model import User, UserRole, Route, Bus, db

driver_bp = Blueprint('driver_bp', __name__)

auth_manager = AuthenticationManager(os.getenv('FLASK_SECRET_KEY'))


@token_required
@driver_bp.route('/', methods=['GET'])
def see_drivers():
    drivers = User.get_all_drivers()

    jsonList = []
    for driver in drivers:
        jsonList.append({
            "id": driver.id,
            "firstname": driver.firstname,
            "middlename": driver.middlename,
            "lastname": driver.lastname,
            "address": driver.address,
            "phonenumber": driver.phonenumber,
            "role": driver.role,
        })

    response = make_response(
        jsonify(jsonList),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response


@token_required
@driver_bp.route('/', methods=['POST'])
def create():
    return redirect(url_for('register'))


@token_required
@driver_bp.route('/<id>', methods=['GET'])
def get():
    driver = User.get_by_id(id)

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

@token_required
@driver_bp.route('<id>/update', methods=['POST'])
def update():
    fname = request.json.get('firstname')
    lname = request.json.get('lastname')
    email = request.json.get('email')
    dob = request.json.get('dob')
    phone = request.json.get('phone')


    driver = User.get_by_id(id)

    driver.firstname = fname
    driver.lastname = lname
    driver.email = email
    driver.dob = dob
    driver.phonenumber = phone

    db.session.commit()


@token_required
@driver_bp.route('/delete', methods=['DELETE'])
def delete():
    return redirect(url_for('delete'))





