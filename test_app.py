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

def test_create_meal_missing_fields(client):
  response = client.post('/meals', json={
    'description': 'Arroz e feijão',
    'date_time': '18/03/2026 12:00'
  })
  assert response.status_code == 400
  assert 'Campos obrigatórios faltando' in response.json['message']

def test_list_meals(client):
  client.post('meals', json={
    'name': 'café',
    'description': 'Café preto',
    'date_time': '18/03/2026 08:00',
    'in_diet': True
  })
  response = client.get('/meals')
  assert response.status_code == 200
  assert len(response.json) >= 1


