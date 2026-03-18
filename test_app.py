import pytest
from app import app
from database import db
from models.meal import Meal

@pytest.fixture
def client():
  app.config['TESTING'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
  with app.test_client() as client:
    with app.app_context():
      db.create_all()
    yield client

def test_create_meal_success(client):
  response = client.post('/meals', json={
      'name': 'Almoço',
      'description': 'Arroz e feijão',
      'date_time': '18/03/2026 12:00',
      'in_diet': True
  })
  assert response.status_code == 200
  assert response.json['name'] == 'Almoço'
