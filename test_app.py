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

def test_get_meal_by_id(client):
  post = client.post('/meals', json={
    'name': 'Jantar',
    'description': 'Salada',
    'date_time': '18/03/2026 19:00',
    'in_diet': False
  })
  meal_id = post.json['id']
  response = client.get(f'/meals/{meal_id}')
  assert response.status_code == 200
  assert response.json[0]['name'] == 'Jantar'

def test_get_meal_not_found(client):
  response = client.get('/meals/999')
  assert response.status_code == 404
  assert 'Refeição não encontrada' in response.json['message']

def test_update_meal_sucess(client):
  post = client.post('/meals', json={
    'name': 'Lanche',
    'description': 'Bolo',
    'date_time': '18/03/2026 16:00',
    'in_diet': True
  })
  meal_id = post.json['id']
  response = client.put(f'/meals/{meal_id}', json={
    'name': 'Lanche Atualizado',
    'in_diet': False
  })
  assert response.status_code == 200
  assert response.json[0]['name'] == 'Lanche Atualizado'

def test_update_meal_not_found(client):
  response = client.put('/meals/999', json={
    'name': 'Lanche Atualizado',
    'in_diet': True
  })
  assert response.status_code == 404
  assert 'Refeição não encontrada' in response.json['message']

def test_delete_meal_success(client):
  post = client.post('/meals', json={
    'name': 'Ceia',
    'description': 'Iogurte',
    'date_time': '18/03/2026 22:00',
    'in_diet': True
  })
  meal_id = post.json['id']
  response = client.delete(f'/meals/{meal_id}')
  assert response.status_code == 200
  assert 'Refeição deletada com sucesso' in response.json['message']

def test_delete_meal_not_found(client):
  response = client.delete('/meals/999')
  assert response.status_code == 404
  assert 'Refeição não encontrada' in response.json['message']

def test_get_meals_by_date(client):
  client.post('/meals', json={
    'name': 'Café da manhã',
    'description': 'Pão e café',
    'date_time': '18/03/2026 08:00',
    'in_diet': True
  })
  response = client.get('/meals/date/18-03-2026')
  assert response.status_code == 200
  assert len(response.json) >= 1

def test_get_meals_by_invalid_date(client):
  response = client.get('/meals/date/01-01-2025')
  assert response.status_code == 200
  assert len(response.json) == 0

def test_get_meals_by_diet(client):
  client.post('/meals', json={
    'name': 'Almoço',
    'description': 'Arroz e feijão',
    'date_time': '18/03/2026 12:00',
    'in_diet': False
  })
  response = client.get('/meals/diet/false')
  assert response.status_code == 200
  assert len(response.json) >= 1

def test_get_meals_by_invalid_diet(client):
  response = client.get('/meals/diet/invalid')
  assert response.status_code == 400
  assert 'Valor inválido para in_diet' in response.json['message']