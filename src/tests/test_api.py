import requests

def test_user_api():
    response = requests.get("https://api.example.com/users")
    assert response.status_code == 200
    
    users = response.json()
    assert len(users) > 0
    assert 'id' in users[0]
    assert 'name' in users[0]
    
    # Проверка создания пользователя
    new_user = {"name": "Test User", "email": "test@example.com"}
    create_response = requests.post("https://api.example.com/users", json=new_user)
    assert create_response.status_code == 201