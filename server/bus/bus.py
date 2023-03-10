import os
from flask import Blueprint, request, make_response, jsonify, json, abort
from auth import AuthenticationManager, token_required, token, current_user
from flask_sqlalchemy import SQLAlchemy

from uuid import uuid4

from model import User, UserRole, Route, Bus, db

bus_bp = Blueprint('bus_bp', __name__)

auth_manager = AuthenticationManager(os.getenv('FLASK_SECRET_KEY'))


class BusManager():
    def modify(self, request_params: dict, bus):
        for param in request_params:
            if param == 'id':
                return make_response(
                    "Unprocessable Entity",
                    401
                )
            bus.__setattr__(param, request_params[param])

        db.session.commit()
        return make_response(
            "Updated Successfully",
            200
        )

bus_manager = BusManager()

@bus_bp.route('/', methods=['GET'])
def see_buses():
    buses = Bus.get_all_buses()

    jsonList = []
    for bus in buses:
        jsonList.append({
            "id": bus.id,
            "capacity": bus.capacity
        })

    response = make_response(
        jsonify(jsonList),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response


@bus_bp.route('/', methods=['POST'])
def create():
    name = request.json.get('name')
    capacity = request.json.get('capacity')

    new_route = Bus(name=name, capacity=capacity)

    db.session.add(new_route)
    db.session.commit()

    return make_response(
        "Bus Created Successfully",
        201
    )

@bus_bp.route('/<id>', methods=['GET'])
def get(id):
    bus = Bus.get(id)

    if bus:
        return jsonify({
            "name": bus.name,
            "capacity": bus.capacity
        })

    return make_response(
        "Bus Not Found",
        404
    )

@bus_bp.route('/update/<id>', methods=['PATCH'])
def update(id):
    bus = Bus.get(id)

    if bus:
        request_params = request.get_json()
        return bus_manager.modify(request_params=request_params, bus=bus)
    
    return make_response(
        "Bus Not Found",
        404
    )

@bus_bp.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    bus = Bus.get(id)

    if bus:
        db.session.delete(bus)
        db.session.commit()

        return ("", 200)
    return make_response(
        "Bus Not Found",
        404
    )

    





