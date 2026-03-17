from database import db
from datetime import datetime

class Meal(db.Model):
  #id, name, description, date_time, in_diet
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  description = db.Column(db.String(200))
  date_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
  in_diet = db.Column(db.Boolean, nullable=False)

# funções auxiliares para converter o objeto Meal em um dicionário e atualizar o objeto a partir de um dicionário
# Método para converter o objeto Meal em um dicionário
  def to_dict(self):
    return{
      'id': self.id,
      'name': self.name,
      'description': self.description,
      'date_time': self.date_time.strftime('%d/%m/%Y %H:%M') if self.date_time else None,
      'in_diet': self.in_diet
    }
# Método para atualizar o objeto Meal a partir de um dicionário
  def update_from_dict(self, data):
    if 'name' in data:
      self.name = data['name']
    if 'description' in data:
      self.description = data['description']
    if 'date_time' in data:
      self.date_time = datetime.strptime(data['date_time'], '%d/%m/%Y %H:%M')
    if 'in_diet' in data:
      self.in_diet = data['in_diet']  