from flask_sqlalchemy import SQLAlchemy

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

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(50))
    dob = db.Column(db.DateTime)
    phonenumber = db.Column(db.String(15))
    role = db.Column(db.Enum(UserRole.CUSTOMER, UserRole.ADMINISTRATOR, UserRole.DRIVER))
    password = db.Column(db.String(128))

    @staticmethod
    def get_by_id(user_id: str):
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
    def get_by_email(user_email: str):
        """Queries User from Databse
        Args:
            user_email (str): user email
        Returns:
            User: user object if found else None"""
        
        try: 
            user = User.query.filter_by(email=user_email).first()
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


    @staticmethod
    def get_all_drivers():
        """Queries All Drivers from Databse
        
        Returns:
            List: list of User objects"""
        
        drivers = User.query.filter_by(
            role=UserRole.DRIVER
        ).all()

        return drivers
    

    @staticmethod
    def get_all_customers():
        """Queries All Customers from Databse
        
        Returns:
            List: list of User objects"""
        
        customers = User.query.filter_by(
            role=UserRole.CUSTOMER
        ).all()

        return customers
    

    def __repr__(self):
        return f"user(id={self.id}, first_name={self.firstname}, last_name={self.lastname}, role={self.role})"



class Bus(db.Model):
    """
    Bus Databse Model

    Parameters:
            id (str): unique id that identifies a single bus
            capacity (int): the number of seats a bus has
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
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
        
    @staticmethod
    def get_all_buses():
        """Gets all Buses
        
        Returns:
            List: list of Bus objects
        """
        buses = Bus.query.all()
        return buses
    

    def __repr__(self):
        return f"Bus(id={self.id}, capacity={self.capacity})"


class Route(db.Model):
    """
    Route Databse Model

    Parameters:
            id (int): unique id that identifies a single route
            source (str): beginning of route
            destination (str): end of route
    """

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50))
    destination = db.Column(db.String(50))
    routename = db.Column(db.String(10))

    @staticmethod
    def get_by_id(route_id: str):
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
        
    @staticmethod
    def get_all_routes():
        """Gets all Routes
        Returns:
            List: list of routes"""
        
        routes = Route.query.all()
        return routes

    @staticmethod
    def get_by_name(name:str):
        """Gets route of given name
        
        Args:
            name (str): route name
        Returns:
            Route object if found, None otherwise"""
        
        try:
            route = Route.query.filter_by(routename=name).first()
            return route
        
        except:
            return None

    def __repr__(self):
        return f"Route(id={self.id}, source={self.source}, destination={self.destination})"



class ScheduledRoute(db.Model):
    """
    Scheduled Routes Databse Model

    Parameters:
            id (int): unique id that identifies a ascheduled route
            routeId (str): unique id that identifies route
            departureTime (datetime): time of bus departure from source
            arrivaltime (datetime): time of bus arrival at destination
    """

    id = db.Column(db.Integer, primary_key=True)
    busId = db.Column(db.Integer, db.ForeignKey(Bus.id))
    routeId = db.Column(db.Integer, db.ForeignKey(Route.id))
    departureTime = db.Column(db.DateTime, default=datetime.now)
    arrivalTime = db.Column(db.DateTime, default=datetime.now)

    bus = db.relationship(Bus, foreign_keys=[busId])
    route = db.relationship(Route, foreign_keys=[routeId])


    @staticmethod
    def get_all_scheduled():
        """Gets all Scheduled Routes
        Returns:
            list: list of scheduled routes
        """

        scheduled_routes = ScheduledRoute.query.all()

        return scheduled_routes


    @staticmethod
    def get_all_assigned(id:int):
        """Gets all Scheduled Routes assigned to a bus

        Args:
            id (int): Bus ID
        Returns:
            list: list of Scheduled Routes"""
        
        try:
            assigned_routes = ScheduledRoute.query.filter(busId=id)
            return assigned_routes
        except:
            return None


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

    id = db.Column(db.String(10), primary_key=True)
    customerId = db.Column(db.String(10), db.ForeignKey(User.id))
    busId = db.Column(db.String(10), db.ForeignKey(Bus.id))
    scheduledRouteId = db.Column(db.String(10), db.ForeignKey(ScheduledRoute.id))
    seatNumber = db.Column(db.Integer)
    purchaseDate = db.Column(db.DateTime, default=datetime.now)


    bus = db.relationship(Bus, foreign_keys=[busId])
    customer = db.relationship(User, foreign_keys=[customerId])
    scheduledRoute = db.relationship(ScheduledRoute, foreign_keys=[scheduledRouteId])


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
    

class Blacklist(db.Model):
    """Invalid Tokens Database Model
    
    Parameters:
            id (int): token id
            token (str): token
    """

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500))


    @staticmethod
    def get(token: str):
        """Gets a token from Database
        
        Args:
            token (str): token
        Returns:
            Blacklist Object If token is found, None otherwise
        """
        blacklist_token = Blacklist.query.filter(Blacklist.token == token).first()

        if blacklist_token:
            return blacklist_token
        else:
            return None
        