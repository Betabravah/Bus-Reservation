import os
from flask import Blueprint, request, make_response, jsonify, json, abort
from auth import AuthenticationManager, token_required, token, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from uuid import uuid4

from model import User, UserRole, Route, Bus, db, ScheduledRoute

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
    
    
    def assign_to_route(self, busId: int, routeId: int, departure, arrival):
        departure = datetime.strptime(departure, '%m/%d/%y %H:%M:%S')
        arrival = datetime.strptime(arrival, '%m/%d/%y %H:%M:%S')
        
        routes = ScheduledRoute.get_all_assigned(busId)

        if routes:
            for route in routes:
                if (route.departureTime <= departure <= route.arrivalTime) or (route.departureTime <= arrival <= route.arrivalTime):
                    return make_response(
                        "Schedule Conflict!",
                        400
                    )
                
        new_schedule = ScheduledRoute(busId=busId, routeId=routeId,
                            departureTime=departure, arrivalTime=arrival)

        db.session.add(new_schedule)
        db.session.commit()

        return make_response(
            "Bus Assigned to Route Successfully",
            201
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

    
@bus_bp.route('/assign', methods=['POST'])
def assign():
    busId = request.json.get('busId')
    routeId = request.json.get('routeId')
    departure = request.json.get('departure-time')
    arrival = request.json.get('arrival-time')

    bus = Bus.get(busId)
    route = Route.get_by_id(routeId)

    if bus and route:
        return bus_manager.assign_to_route(busId, routeId, departure, arrival)
    return make_response(
        "Not Found",
        404
    )
    





