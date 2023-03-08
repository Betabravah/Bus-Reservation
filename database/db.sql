drop database if EXISTS brs;

create database brs;

use brs;


create table Bus (
    id varchar(10) primary key not null,
    capacity int not null        
);

create table User (
    id int primary key auto_increment not null,
    firstname varchar(50) not null,
    lastname varchar(50) not null,
    email varchar(50) not null,
    dob datetime,
    phonenumber varchar(15),
    `role` Enum('CUSTOMER', 'ADMINISTRATOR', 'DRIVER'),
    `password` varchar(128)
);

create table Route (
    id varchar(10) primary key not null,
    source varchar(50) not null,
    destination varchar(50) not null
)


create table ScheduledRoute (
    id varchar(10) primary key not null,
    busId varchar(10) not null,
    routeId varchar(10) not null,
    departureTime datetime not null,
    arrivalTime datetime not null,

    foreign key (busId) references Bus(id),
    foreign key (routeId) references `Route`(id)

);


create table Reservation (
    id varchar(10) primary key not null,
    customerId varchar(10) not null,
    busId varchar(10) not null,
    scheduledRouteId varchar(10) not null,
    seatNumber int not null,
    purchaseDate datetime not null,

    foreign key (customerId) references customer(id),
    foreign key (busId) references bus(id),
    foreign key (scheduledRouteId) references ScheduledRoute(id)
);


create table Blacklist (
    id int primary key auto_increment not null,
    token varchar(500) not null,
    expiry datetime not null
);