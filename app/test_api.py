import requests
from pprint import pprint

BASE_URL = "http://127.0.0.1:8000"  # Убрали /api, так как он уже в роутерах

def test_api():
    # 1. Регистрация (теперь путь /api/register)
    print("\n1. Регистрируем пользователя:")
    reg_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/api/register", json=reg_data)
    
    if response.status_code != 200:
        print(f"Ошибка регистрации: {response.status_code}")
        pprint(response.json())
        return
    
    pprint(response.json())

    # 2. Авторизация
    print("\n2. Получаем токен:")
    auth_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/api/token", data=auth_data)
    
    if response.status_code != 200:
        print(f"Ошибка авторизации: {response.status_code}")
        pprint(response.json())
        return
    
    token = response.json().get("access_token")
    print(f"Токен: {token[:15]}...")

    # 3. Получение профиля
    print("\n3. Получаем профиль:")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/users/me", headers=headers)
    pprint(response.json())

    # 4. Пополнение баланса
    print("\n4. Пополняем баланс на 100:")
    response = requests.post(
        f"{BASE_URL}/api/balance/deposit?amount=100",
        headers=headers
    )
    pprint(response.json())

if __name__ == "__main__":
    test_api()