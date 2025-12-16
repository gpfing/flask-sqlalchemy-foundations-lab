# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    quake = Earthquake.query.get(id)
    if quake:
        body = {
            "id": quake.id,
            "magnitude": quake.magnitude,
            "location": quake.location,
            "year": quake.year
        }
        return make_response(body, 200)
    else:
        return make_response({"message": f"Earthquake {id} not found."}, 404)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quake_list = []
    for quake in quakes:
        quake_dict = {
            'id': quake.id,
            'magnitude': quake.magnitude,
            'location': quake.location,
            'year': quake.year
        }
        quake_list.append(quake_dict)
    
    body = {
        'count': len(quake_list),
        'quakes': quake_list
    }
    return make_response(body, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
