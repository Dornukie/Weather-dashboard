from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db, User, City, Temperature
import requests
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)  # Initialize JWTManager with the Flask app

def create_tables():
    db.create_all()

@app.route('/')
def home():
    return "Welcome to the Weather Dashboard API!"

# POST /register - Register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'User already exists'}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# POST /login - User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# POST /cities - Save a favorite city
@app.route('/cities', methods=['POST'])
@jwt_required()  # Require JWT authentication for this endpoint
def add_city():
    data = request.get_json()
    city_name = data.get('city_name')

    if City.query.filter_by(name=city_name).first():
        return jsonify({'error': 'City already exists'}), 400

    city = City(name=city_name)
    db.session.add(city)
    db.session.commit()

    return jsonify({'message': 'City added successfully'}), 201

# GET /cities - Get all saved cities
@app.route('/cities', methods=['GET'])
@jwt_required()  # Require JWT authentication for this endpoint
def get_cities():
    cities = City.query.all()
    result = [{'id': city.id, 'name': city.name} for city in cities]

    return jsonify(result)

# POST /temps - Save temperatures of various cities
@app.route('/temps', methods=['POST'])
@jwt_required()  # Require JWT authentication for this endpoint
def add_temp():
    data = request.get_json()
    city_id = data.get('city_id')
    temperature = data.get('temperature')

    temp = Temperature(city_id=city_id, temperature=temperature, timestamp=datetime.utcnow())
    db.session.add(temp)
    db.session.commit()

    return jsonify({'message': 'Temperature saved successfully'}), 201

# GET /temps - Get all saved temperatures
@app.route('/temps', methods=['GET'])
@jwt_required()
def get_temps():
    try:
        temps = Temperature.query.all()
        result = [{'id': temp.id, 'temperature': temp.temperature, 'timestamp': temp.timestamp} for temp in temps]
        return jsonify(result)
    except Exception as e:
        print(f"Error in get_temps endpoint: {e}")
        return jsonify({'message': 'Internal server error'}), 500


# GET /city/temp/<id> - Get the temp of a specific city by city ID
@app.route('/city/temp/<int:id>', methods=['GET'])
@jwt_required()
def get_city_temp(id):
    try:
        temps = Temperature.query.filter_by(city_id=id).all()
        if not temps:
            return jsonify({'message': 'No temperatures found for the specified city ID'}), 404

        result = [{'temperature': temp.temperature, 'timestamp': temp.timestamp} for temp in temps]
        return jsonify(result)
    except Exception as e:
        print(f"Error in get_city_temp endpoint: {e}")
        return jsonify({'message': 'Internal server error'}), 500


# GET /weather - Get current weather for saved cities using OpenWeather API
@app.route('/weather', methods=['GET'])
@jwt_required()  # Require JWT authentication for this endpoint
def get_weather():
    cities = City.query.all()
    api_key = app.config['WEATHER_API_KEY']
    weather_data = []

    for city in cities:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={api_key}')
        data = response.json()
        weather_data.append({
            'city': city.name,
            'temperature': data['main']['temp'],
            'weather': data['weather'][0]['description']
        })

    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
