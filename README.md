# Welcome to Team 8's Potato Rooms Repo!
Created for CS302 IT Solution Development, PotatoRooms is a microservice-based web application that enables event organizers to easily find and book venues for their events.

This project consists of 7 different microservices: Rooms, Customers, Bookings, Room-Booking (composite), User Interface (composite), Notifications & Stripe (composite). This way, the application is highly decoupled and it is also easier to insert new functionalities in future.

## Setting up the DB:
1. Ensure that your MAMP/WAMP is on.
2. Create a user cs302 with password cs302 using phpmyadmin.
3. Create a connection with host localhost and port 3306, user cs302, password cs302.
4. Load the merged.merged.sql file into mySQL


## Running the services locally on DockerCompose:
Make sure you are in the projects (root) directory 
```docker compose up -d --build```

When you are done running the services:   
```docker compose down```

## Using Waitress as a WSGI server for atomic services:

> Atomic Services: Rooms, Customers, Bookings  
> Composite Services: Room-Bookings, Stripe, User Interface

```
cd src
pip install waitress
waitress-serve --port <service port number> <service flask file name>:app
```

So for example if running for rooms ->   
```waitress-serve --port 30000 app:app```

## Accessing the UI:  
To access our UI -> http://localhost:8081  
To access rooms -> http://localhost:30000/rooms  
To access customers -> http://localhost:31000/customer  
To access bookings -> http://localhost:32000/bookings  
To access stripe -> http://localhost:4242

## Notifications
To check if notification is sent: 
1. Go to project_notifications_1 container.
2. Look at the logs. 
3. If success, it will print successful and the email.