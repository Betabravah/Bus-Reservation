from flask import json, abort
from werkzeug.exceptions import HTTPException

from flask import Blueprint, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from uuid import uuid4


from model import User, UserRole, Route, Bus, ScheduledRoute, db

route_bp = Blueprint('route_bp', __name__)


@route_bp.route('/', methods=['GET'])
def see_routes():
    routes = Route.get_all_routes()

    jsonList = []
    for route in routes:
        jsonList.append({
            "id": route.id,
            "source": route.source,
            "destination": route.destination
        })

    response = make_response(
        jsonify(jsonList),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response


@route_bp.route('/', methods=['POST'])
def add():
    id = uuid4()
    source = request.form.get('source')
    destination = request.form.get('destination')

    new_route = Route(id=id, source=source, destination=destination)

    db.session.add(new_route)
    db.session.commit()


@route_bp.route('/scheduledroutes', mehtods=['POST'])
def schedule():
    if current_user.role == UserRole.ADMINISTRATOR:
        id = uuid4()
        busId = request.form.get('busId')
        routeId = request.form.get('routeId')
        departureTime = request.form.get('departureTime')
        arrivalTime = request.form.get('arrivalTime')

        new_scheduled_route = ScheduledRoute(id=id, busId=busId, 
                                            routeId=routeId, departureTime=departureTime,
                                            arrivalTime=arrivalTime)
        
        db.session.add(new_scheduled_route)
        db.commit()
    

@route_bp('/scheduledroutes', methods=['GET'])
def see_scheduled_routes():
    routes = ScheduledRoute.get_all_scheduled()

    jsonList = []
    for route in routes:
        jsonList.append({
            "id": route.id,
            "busId": route.busId,
            "routeId": route.routeId,
            "departureTime": route.departuretime,
            "arrivalTime": route.arrivalTime
        })

    response = make_response(
        jsonify(jsonList),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response
