import os
from flask import Flask

from route import route_bp
from bus import bus_bp
from driver import driver_bp
from customer import customer_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')


app.register_blueprint(route_bp, url_prefix='/routes')
app.register_blueprint(bus_bp, url_prefix='/buses')
app.register_blueprint(driver_bp, url_prefix='/drivers')
app.register_blueprint(customer_bp, url_prefix='/customers')


@app.route('/')
def home():
    return



if __name__ == "__main__":
    app.run(debug=True)