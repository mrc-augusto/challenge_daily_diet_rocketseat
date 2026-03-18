import pytest
from app import app, db
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
    client.post('/meals', json={
        'name': 'Café', 'description': 'Café preto', 'date_time': '18/03/2026 08:00', 'in_diet': True
    })
    response = client.get('/meals')
    assert response.status_code == 200
    assert len(response.json) >= 1

def test_get_meal_by_id(client):
    post = client.post('/meals', json={
        'name': 'Jantar', 'description': 'Salada', 'date_time': '18/03/2026 19:00', 'in_diet': False
    })
    meal_id = post.json['id']
    response = client.get(f'/meals/{meal_id}')
    assert response.status_code == 200
    assert response.json[0]['name'] == 'Jantar'

def test_get_meal_not_found(client):
    response = client.get('/meals/999')
    assert response.status_code == 404
    assert 'Refeição não encontrada' in response.json['message']

def test_update_meal_success(client):
    post = client.post('/meals', json={
        'name': 'Lanche', 'description': 'Bolo', 'date_time': '18/03/2026 16:00', 'in_diet': True
    })
    meal_id = post.json['id']
    response = client.put(f'/meals/{meal_id}', json={
        'name': 'Lanche Atualizado', 'in_diet': False
    })
    assert response.status_code == 200
    assert response.json[0]['name'] == 'Lanche Atualizado'

def test_update_meal_not_found(client):
    response = client.put('/meals/999', json={
        'name': 'Qualquer', 'in_diet': True
    })
    assert response.status_code == 404
    assert 'Refeição não encontrada' in response.json['message']

def test_delete_meal_success(client):
    post = client.post('/meals', json={
        'name': 'Ceia', 'description': 'Leite', 'date_time': '18/03/2026 23:00', 'in_diet': True
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
        'name': 'Café', 'description': 'Café preto', 'date_time': '18/03/2026 08:00', 'in_diet': True
    })
    response = client.get('/meals/date/18-03-2026')
    assert response.status_code == 200
    assert len(response.json) >= 1

def test_get_meals_by_invalid_date(client):
    response = client.get('/meals/date/2026-03-18')
    assert response.status_code == 400
    assert 'Formato de data inválido' in response.json.get('mesage', '')

def test_get_meals_by_diet(client):
    client.post('/meals', json={
        'name': 'Café', 'description': 'Café preto', 'date_time': '18/03/2026 08:00', 'in_diet': True
    })
    response = client.get('/meals/diet/true')
    assert response.status_code == 200
    assert all(meal['in_diet'] for meal in response.json)

def test_get_meals_by_invalid_diet(client):
    response = client.get('/meals/diet/invalid')
    assert response.status_code == 400
    assert 'Valor inválido para in_diet' in response.json['message']

def test_validate_required_fields():
    from utils import validate_required_fields
    data = {'name': '', 'in_diet': None}
    missing = validate_required_fields(data, ['name', 'in_diet'])
    assert 'name' in missing and 'in_diet' in missing

def test_meal_model_methods():
    meal = Meal(name='Teste', description='Desc', date_time='18/03/2026 10:00', in_diet=True)
    d = meal.to_dict()
    assert d['name'] == 'Teste'
    meal.update_from_dict({'name': 'Novo', 'in_diet': False})
    assert meal.name == 'Novo'
    assert meal.in_diet is False