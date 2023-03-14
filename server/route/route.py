from flask import json, abort
from werkzeug.exceptions import HTTPException

from flask import Blueprint, request, make_response, jsonify
from uuid import uuid4


from model import User, UserRole, Route, Bus, ScheduledRoute, db

route_bp = Blueprint('route_bp', __name__)



class RouteManager():
    def modify(self, request_params: dict, route):
        for param in request_params:
            if param == 'id':
                return make_response(
                    "Unprocessable Entity",
                    401
                )
            route.__setattr__(param, request_params[param])
        
        # new_route_name = route.'source'[:3] + '-' + route['destination'][:3]
        # existing_route = Route.get_by_name(new_route_name)
        # if existing_route:
        #     return make_response(
        #         "Route Already Exists",
        #         400
        #     )

        # route.__setattr__("routename", new_route_name)
        db.session.commit()
        return make_response(
            "Updated Successfully",
            200
        )

route_manager = RouteManager()

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
def create():
    source = request.json.get('source')
    destination = request.json.get('destination')
    routename = source[:3] + '-' + destination[:3]

    route = Route.get_by_name(routename)
    if route:
        return make_response(
            "Route Already Exists",
            400
        )

    new_route = Route(routename=routename, source=source, destination=destination)

    db.session.add(new_route)
    db.session.commit()

    return make_response(
        "Route Created Successfully",
        201
    )

@route_bp.route('/update/<id>', methods=['PATCH'])
def update(id):
    route = Route.get_by_id(id)
    if route:
        request_params = request.get_json()
        return route_manager.modify(request_params=request_params, route=route)
    
    return make_response(
        "Route Not Found",
        404
    )


@route_bp.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    route = Route.get_by_id(id)

    if route:
        db.session.delete(route)
        db.session.commit()

        return ("", 200)
    return make_response(
        "Route Not Found",
        404
    )

@route_bp.route('/reserve', methods=['POST'])
def reserve():
    busId = request.json.get('busId')


@route_bp.route('/scheduledroutes', methods=['POST'])
def schedule():
    if current_user.role == UserRole.ADMINISTRATOR:
        id = uuid4()
        busId = request.json.get('busId')
        routeId = request.json.get('routeId')
        departureTime = request.json.get('departureTime')
        arrivalTime = request.json.get('arrivalTime')

        new_scheduled_route = ScheduledRoute(id=id, busId=busId, 
                                            routeId=routeId, departureTime=departureTime,
                                            arrivalTime=arrivalTime)
        
        db.session.add(new_scheduled_route)
        db.commit()
    

@route_bp.route('/scheduledroutes', methods=['GET'])
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
