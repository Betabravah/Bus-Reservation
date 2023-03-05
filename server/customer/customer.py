from flask import Blueprint, request, make_response, jsonify, json, abort
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
import bcrypt


from model import User, UserRole, Route, Bus, db

customer_bp = Blueprint('customer_bp', __name__)



@customer_bp.route('/', methods=['GET'])
def see_customers():
    customers = User.get_all_customers()

    jsonList = []
    for customer in customers:
        jsonList.append({
            "id": customer.id,
            "firstname": customer.firstname,
            "middlename": customer.middlename,
            "lastname": customer.lastname,
            "address": customer.address,
            "phonenumber": customer.phonenumber,
            "role": customer.role,
        })

    response = make_response(
        jsonify(jsonList),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response


@customer_bp.route('/register', methods=['POST'])
def add():
    id = uuid4()
    firstname = request.form.get('firstname')
    middlename = request.form.get('middlename')
    lastname = request.form.get('lastname')
    address = request.form.get('address')
    phonenumber = request.form.get('phonenumber')
    password = request.form.get('password')
    

    new_customer = User(id=id,
                      firstname=firstname,
                      middlename=middlename,
                      lastname=lastname,
                      address=address,
                      phonenumber=phonenumber,
                      role=UserRole.CUSTOMER,
                      password=bcrypt.hashpw(password, bcrypt.gensalt()))

    db.session.add(new_customer)
    db.session.commit()

