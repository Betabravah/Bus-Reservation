from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from datetime import datetime

db = SQLAlchemy()


class UserRole:
    """Data class that represents the roles of users involved in the system"""

    CUSTOMER = 'CUSTOMER'
    ADMINISTRATOR = 'ADMINISTRATOR'
    DRIVER = 'DRIVER'


class User:
    """
    User Database Model 
    
    Parameters:
            id (str): unique id to identify single user
            password (str): user's hashed password
            role (str): user's role type in the system
            firstname (str): first name of user
            middlename (str): middle name of user
            lastname (str): last name of user
            address (str): address of user
            phonenumber (str): phone number of user
    """

    id = db.Column(db.String(10), primary_key=True)
    password = db.Column(db.String(128))
    role = db.Column(db.Enum(UserRole.CUSTOMER, UserRole.ADMINISTRATOR, UserRole.DRIVER))
    firstname = db.Column(db.String(50))
    middlename = db.Coulmn(db.String(50))
    lastname = db.Column(db.String(50))
    address = db.Coulmn(db.String950)
    phonenumber = db.Coulmn(db.String(15))



class Bus(db.Model):
    """
    Bus Databse Model

    Parameters:
            id (str): unique id that identifies a single bus
            capacity (int): the number of seats a bus has
    """

    id = db.Column(db.String(10), primary_key=True)
    capacity = db.Column(db.Integer)



class Route(db.Model):
    """
    Route Database Model

    Parameters:
            id (str): unique id that identifies a single route
            source (str): beginning of route
            destination (str): end of route
    """

    id = db.Column(db.String(10), primary_key=True)
    source = db.Column(db.String(50))
    destination = db.Column9db.String(50)



class ScheduledRoute(db.Model):
    """
    Scheduled Routes Databse Model

    Parameters:
            id (str): unique id that identifies a ascheduled route
            routeId (str): unique id that identifies route
            departureTime (datetime): time of bus departure from source
            arrivaltime (datetime): time of bus arrival at destination
    """

    id = db.Column(db.String(10), primary_key=True)
    routeId = db.clumn(db.String(10), db.ForiegnKey(Route.id))
    departureTime = db.Column(db.DateTime, default=datetime.now)
    arrivalTime = db.Column(db.Datetime)

    route = db.relationship(Route, foriegn_key=[routeId])


class Reservation:
    """
    Reservation Databse Model

    Parameters:
            id (str): unique id that identifies a single reservation
            customerId (str): unique id that identifies the owner of the reservation
            busId (str): unique id that identifies the bus the reservation is made on
            scheduledRouteId (str): unique id that identifies a scheduled route the reservation is made on
            seatNumber (int): seat of reservation
            purchaseDate (datetime): time of reservation
    """

    id = db.Coulmn(db.String(10))
    customerId = db.Coulmn(db.String(10), db.ForiegnKey((User.id)))
    busId = db.Column(db.String(10), db.ForiegnKey(Bus.id))
    scheduledRouteId = db.Column(db.String(10), db.ForiegnKey(Route.id))
    seatNumber = db.Coulmn(db.Integer)
    purchaseDate = db.Column(db.Datetime, default=datetime.now)


    bus = db.relationship(Bus, foriegn_keys=[busId])
    scheduledRouteId = db.relationship(ScheduledRoute, foriegn_key=[scheduledRouteId])