import random
import requests
from pprint import pprint

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    rand_suffix = random.randint(1000, 9999)

    print("\n1. Регистрируем пользователя:")
    reg_data = {
        "email": f"test{rand_suffix}@example.com",
        "username": f"testuser{rand_suffix}",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=reg_data)

    if response.status_code != 200:
        print(f"Ошибка регистрации: {response.status_code}")
        try:
            pprint(response.json())
        except:
            print(response.text)
        return

    pprint(response.json())

    print("\n2. Получаем токен:")
    auth_data = {
        "username": reg_data["username"],
        "password": reg_data["password"]
    }
    response = requests.post(f"{BASE_URL}/auth/token", data=auth_data)

    if response.status_code != 200:
        print(f"Ошибка авторизации: {response.status_code}")
        try:
            pprint(response.json())
        except:
            print(response.text)
        return

    token = response.json().get("access_token")
    print(f"Токен: {token[:15]}...")

    print("\n3. Получаем профиль:")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/users/me", headers=headers)
    pprint(response.json())

    print("\n4. Пополняем баланс на 100:")
    response = requests.post(
        f"{BASE_URL}/api/balance/deposit?amount=100",
        headers=headers
    )
    pprint(response.json())

if __name__ == "__main__":
    test_api()
