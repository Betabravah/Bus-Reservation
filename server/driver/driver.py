from flask import Blueprint, request, make_response, jsonify, json, abort
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4


from model import User, UserRole, Route, Bus, db

driver_bp = Blueprint('driver_bp', __name__)



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


@driver_bp.route('/', methods=['POST'])
def add():
    id = uuid4()
    firstname = request.form.get('firstname')
    middlename = request.form.get('middlename')
    lastname = request.form.get('lastname')
    address = request.form.get('address')
    phonenumber = request.form.get('phonenumber')
    

    new_driver = User(id=id,
                      firstname=firstname,
                      middlename=middlename,
                      lastname=lastname,
                      address=address,
                      phonenumber=phonenumber,
                      role=UserRole.DRIVER)

    db.session.add(new_driver)
    db.session.commit()

