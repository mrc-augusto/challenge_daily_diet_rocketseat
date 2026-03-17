from flask import Flask, request, jsonify
from config import DATABASE_URI
from models.meal import Meal
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/meals', methods=['POST'])
def create_meal():
  data=request.json
  meal = Meal(
    name=data.get('name'),
    description=data.get('description'),
    date_time=data.get('date_time'),
    in_diet=data.get('in_diet')
  )
  db.session.add(meal)
  db.session.commit()
  return jsonify(meal.to_dict())
  
@app.route('/meals', methods=['GET'])
def list_meals():
  meals = Meal.query.all()
  return jsonify([meal.to_dict() for meal in meals])

@app.route('/meals/<int:id>', methods=['GET'])
def get_meal(id):
  meal = Meal.query.get_or_404(id)
  return jsonify(meal.to_dict())



@app.route('/hello-world', methods=['GET'])
def hello_world():
  return 'Hello World!'

if __name__ == '__main__':
  app.run(debug=True)