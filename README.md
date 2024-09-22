Weather Dashboard API
Description
The Weather Dashboard API is a Flask-based application that allows users to register, authenticate, and manage their favorite cities and temperatures. It integrates with the OpenWeather API to provide current weather data for saved cities.

Features
User Authentication: Register and log in users securely.
Favorite Cities: Save and retrieve a list of favorite cities.
Temperature Management: Save and retrieve temperatures for various cities at different times.
Current Weather: Fetch current weather conditions for saved cities.
API Endpoints
User Authentication
POST /register: Register a new user.
POST /login: Authenticate a user.
City Management
POST /cities: Save a favorite city.
GET /cities: Retrieve a list of saved cities.
Temperature Management
POST /temps: Save temperatures for various cities at different times.
GET /temps: Retrieve a list of saved temperatures along with their timestamps.
GET /city/temp/{id}: Get the temperature of a specific city by its ID.
Weather Data
GET /weather: Get the current weather for saved cities using the OpenWeather API.
Database Models
User: Represents registered users.
City: Represents saved cities.
Temperature: Represents temperature readings for various cities.
