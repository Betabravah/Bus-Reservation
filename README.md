# Bus Reservation System
  Bus reservation system is a system that intends to automate the management of buses for bus companies and streamline ticket buying process for customers.   

  The system provides 24/7 service thus customers can
buy tickets whenever they want. It also provides real time bus and seat availability information for
customers.  

  For Bus Company, the system provides the ability to effectively manage its resources. The company can
add employee and bus information to the system, keep track of available buses, create and schedule
routes with start and end destinations, allocate drivers and buses to each routes and get insight about the
performance of the whole process using the system.  

  Using the system, customers can view available buses, reserve seat and cancel reservation.  

## Functional Requirements
### User registration<a id='fr-01'></a>
- ID: FR-01
- Summary – the system allows new users to be registered to the system
- Dependency: None

### Login <a id='fr-02'></a>
- ID: FR-02
- Summary – the system allows user to login using user id and password
- Dependency: [FR-01](#fr-01)

### View available buses <a id='fr-03'></a>
- ID: FR-03
- Summary – the system allows customers to view available buses
- Dependency: [FR-01](#fr-01) and [FR-02](#fr-02)

### Reserve seat <a id='fr-04'></a>
- ID: FR-04
- Summary – the system allows customers to reserve seat for travel
- Dependency: [FR-01](#fr-01), [FR-02](#fr-02) and [FR-03](#fr-03)

### Cancel reservation <a id='fr-05'></a>
- ID: FR-05
- Summary – the system allows customers to cancel reservation
- Dependency: [FR-01](#fr-01), [FR-02](#fr-02) and [FR-04](#fr-04)

### Add driver <a id='fr-06'></a>
- ID: FR-06
- Summary – the system allows administrator to add driver information
- Dependency: [FR-01](#fr-01) and [FR-02](#fr-02)

### Add bus <a id='fr-07'></a>
- ID: FR-07
4 | P a g e
- Summary – the system allows administrator to add bus information
- Dependency: [FR-01](#fr-01) and [FR-02](#fr-02)

### Create routes <a id='fr-08'></a>
- ID: FR-08
- Summary – the system allows administrator to add route information
- Dependency: [FR-01](#fr-01) and [FR-02](#fr-02)

### Search <a id='fr-09'></a>
- ID: FR-09
- Summary – the system allows administrator to find a specified customer, bus or route
- Dependency: [FR-01](#fr-01) and [FR-02](#fr-02)

### Assign drivers to buses <a id='fr-10'></a>
- ID: FR-10
- Summary – the system allows administrator to assign available driver to a bus
- Dependency: [FR-01](#fr-01), [FR-02](#fr-02), [FR-06](#fr-06) and [FR-07](#fr-07)

### Assign buses to routes <a id='fr-11'></a>
- ID: FR-11
- Summary – the system allows administrator to assign available bus to routes
- Dependency: [FR-01](#fr-01), [FR-02](#fr-02), [FR-07](#fr-07) and [FR-08](#fr-08)

### Generate report <a id='fr-12'></a>
- ID: FR-12
- Summary – the system allows administrator to view customer, bus, driver and route status
- Dependency: [FR-01](#fr-01) and [FR-02](#fr-02)