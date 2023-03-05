drop database if EXISTS brs;

create database brs;

use brs;


create table Bus (
    id varchar(10) primary key,
    capacity int not null        
);

create table User (
    id varchar(10) primary key,
    firstname varchar(50) not null,
    middlename varchar(50) not null,
    lastname varchar(50) not null,
    phonenumber varchar(15),
    `role` Enum('CUSTOMER', 'ADMINISTRATOR', 'DRIVER'),
    `password` varchar(128)
);

create table Route (
    id varchar(10) primary key,
    source varchar(50) not null,
    destination varchar(50) not null
)


create table ScheduledRoute (
    id varchar(10) primary key,
    busId varchar(10) not null,
    routeId varchar(10) not null,
    departureTime datetime not null,
    arrivalTime datetime not null,

    foreign key (busId) references Bus(id),
    foreign key (routeId) references `Route`(id)

);


create table Reservation (
    id varchar(10) primary key,
    customerId varchar(10) not null,
    busId varchar(10) not null,
    scheduledRouteId varchar(10) not null,
    seatNumber int not null,
    purchaseDate datetime not null,

    foreign key (customerId) references customer(id),
    foreign key (busId) references bus(id),
    foreign key (routeId) references ScheduledRoute(id)
);

