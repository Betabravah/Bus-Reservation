from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from datetime import datetime

db = SQLAlchemy()


class UserRole:
    """Data class that represents the roles of users involved in the system"""

    CUSTOMER = 'CUSTOMER'
    ADMINISTRATOR = 'ADMINISTRATOR'
    DRIVER = 'DRIVER'


class User(db.Model):
    """
    User Databse Model 
    
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
    address = db.Coulmn(db.String(50))
    phonenumber = db.Coulmn(db.String(15))

    @staticmethod
    def get(user_id: str):
        """Queries User from Databse
        Args:
            user_id (str): user id
        Returns:
            User: user object if found else None"""
        
        try: 
            user = User.query.filter_by(id=user_id).first()
            return user
        except:
            return None
        

    @staticmethod
    def get_driver(driver_id: str):
        """Queries Driver from Databse
        Args:
            driver_id (str): driver id
        Returns:
            User: user object if found else None"""
        
        try:
            driver = User.query.filter_by(
                id=driver_id,
                role=UserRole.DRIVER
            ).first()

            return driver
        except:
            return None
        
    @staticmethod
    def get_customer(customer_id: str):
        """Queries Customer from Databse
        Args:
            customer_id (str): cusomer id
        Returns:
            Customer: User object if found else None"""
        
        try:
            customer = User.query.filter_by(
                id=customer_id,
                role=UserRole.CUSTOMER
            ).first()
            return customer
        except:
            return None


    def __repr__(self):
        return f"user(id={self.id}, first_name={self.firstname}, last_name={self.lastname}, role={self.role})"

    
    


class Bus(db.Model):
    """
    Bus Databse Model

    Parameters:
            id (str): unique id that identifies a single bus
            capacity (int): the number of seats a bus has
    """

    id = db.Column(db.String(10), primary_key=True)
    capacity = db.Column(db.Integer)


    @staticmethod
    def get(bus_id: str):
        """Queries bus from Databse
        Args:
            bus_id (str): bus id
        Returns:
            Bus: Bus object if found else None
        """
        try:
            bus = Bus.query.filter_by(id=bus_id).first()
            return bus
        except:
            return None

    def __repr__(self):
        return f"Bus(id={self.id}, capacity={self.capacity})"


class Route(db.Model):
    """
    Route Databse Model

    Parameters:
            id (str): unique id that identifies a single route
            source (str): beginning of route
            destination (str): end of route
    """

    id = db.Column(db.String(10), primary_key=True)
    source = db.Column(db.String(50))
    destination = db.Column(db.String(50))

    @staticmethod
    def get(route_id: str):
        """Queries route from Databse
        
        Args:
            route_id: route id
        
        Returns:
            Route: Route object if found else None"""
        try:
            route = Route.query.filter_by(id=route_id).first()
            return route
        except:
            return None


    def __repr__(self):
        return f"Route(id={self.id}, source={self.source}, destination={self.destination})"



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
    busId = db.Column(db.String(10), db.ForiegnKey(Bus.id))
    routeId = db.clumn(db.String(10), db.ForiegnKey(Route.id))
    departureTime = db.Column(db.DateTime, default=datetime.now)
    arrivalTime = db.Column(db.Datetime)

    bus = db.relationship(Bus, foriegn_key=[busId])
    route = db.relationship(Route, foriegn_key=[routeId])


    @staticmethod
    def get_all_scheduled():
        """Gets all Scheduled Routes
        Returns:
            list: list of schuduled routes
        """

        scheduled_routes = ScheduledRoute.query.all()

        return scheduled_routes

    def __repr__(self):
        return f"Scheduled-Route(id={self.id}, bus={self.busId} route={self.routeId}, departure={self.departureTime}, arrival={self.arrivalTime})"

class Reservation(db.Model):
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


    @staticmethod
    def tickets(owner_id: str):
        """Gets all reservations of a user

        Returns:
            list: list of reservation objects
        
        """

        tickets = Reservation.query.filter(
                Reservation.owner_id == owner_id
        )

        return tickets


    @staticmethod
    def cancel(id: str):
        """ Cancels a reservation of a user 
        Args:
            id (str): reservation id
            
        Returns:
            None
        """

        Reservation.query.filter_by(id=id).delete()

    def __repr__(self):
        return f"Resevation(id={self.id}, reservation_by={self.customerId}, route={self.scheduledRouteId}, seat_number={self.seatNumber})"