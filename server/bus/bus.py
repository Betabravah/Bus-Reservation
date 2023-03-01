from flask import Blueprint, request, make_response, jsonify, json, abort
from flask_sqlalchemy import SQLAlchemy

from uuid import uuid4

from model import User, UserRole, Route, Bus, db

bus_bp = Blueprint('bus_bp', __name__)



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
def add():
    id = uuid4()
    capacity = request.form.get('capacity')

    new_route = Route(id=id, capacity=capacity)

    db.session.add(new_route)
    db.session.commit()

