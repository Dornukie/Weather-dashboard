class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'my_actual_secret_key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///my_actual_weather.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY') or 'my_actual_openweather_api_key'

