from flask import Flask, request, jsonify
from config import DATABASE_URI
from models.meal import Meal
from utils import jsonify_meals, validate_required_fields
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/meals', methods=['POST'])
def create_meal():
  data=request.json
  from datetime import datetime
  date_time = data.get('date_time')
  if date_time:
    try:
      date_time = datetime.strptime(date_time, '%d/%m/%Y %H:%M')
    except ValueError:
      return jsonify({'message': 'Formato de data inválido. Use dd/mm/yyyy HH:MM'}), 400
  meal = Meal(
    name=data.get('name'),
    description=data.get('description'),
    date_time=date_time,
    in_diet=data.get('in_diet')
  )

  missing = validate_required_fields(data, ['name', 'in_diet'])
  if missing:
    return jsonify({'message': f'Campos obrigatórios faltando: {', '.join(missing)}'}), 400

  db.session.add(meal)
  db.session.commit()
  return jsonify(meal.to_dict())
  
@app.route('/meals', methods=['GET'])
def list_meals():
  meals = Meal.query.all()
  return jsonify_meals(meals)

@app.route('/meals/<int:id>', methods=['GET'])
def get_meal(id):
  meal = Meal.query.get(id)
  if not meal:
    return jsonify({'message': 'Refeição não encontrada'}), 404
  return jsonify_meals([meal])

@app.route('/meals/<int:id>', methods=['PUT'])
def update_meal(id):
  meal = Meal.query.get(id)
  if not meal:
    return jsonify({'message': 'Refeição não encontrada'}), 404
  
  data = request.json
  name = data.get('name', meal.name)
  description = data.get('description', meal.description)
  in_diet = data.get('in_diet', meal.in_diet)

  missing = validate_required_fields(data, ['name', 'in_diet'])
  if missing:
    return jsonify({'message': f'Campos obrigatórios faltando: {', '.join(missing)}'}), 400

  meal.name = name
  meal.description = description
  meal.in_diet = in_diet

  db.session.commit()
  return jsonify_meals([meal])

@app.route('/meals/<int:id>', methods=['DELETE'])
def delete_meal(id):
  meal = Meal.query.get(id)
  if not meal:
    return jsonify({'message': 'Refeição não encontrada'}), 404
  
  db.session.delete(meal)
  db.session.commit()
  return jsonify({'message': 'Refeição deletada com sucesso'})

@app.route('/meals/date/<date>', methods=['GET'])
def get_meals_by_date(date):
  from datetime import datetime
  try:
    date_obj = datetime.strptime(date, '%d-%m-%Y').date()
  except ValueError:
    return jsonify({'mesage': 'Formato de data inválido. Use dd-mm-yyyy'}),400

  start = datetime(date_obj.year, date_obj.month, date_obj.day, 0, 0, 0)
  end = datetime(date_obj.year, date_obj.month, date_obj.day, 23, 59, 59)

  meals = Meal.query.filter(Meal.date_time >= start, Meal.date_time <= end).all()

  return jsonify_meals(meals)

@app.route('/meals/diet/<in_diet>', methods=['GET'])
def get_meals_by_diet(in_diet):
  if in_diet.lower() not in ['true', 'false']:
    return jsonify({'message': 'Valor inválido para in_diet. Use true ou false'}), 400
  
  meals = Meal.query.filter_by(in_diet=in_diet.lower() == 'true').all()
  return jsonify_meals(meals)
  
if __name__ == '__main__':
  app.run(debug=True)