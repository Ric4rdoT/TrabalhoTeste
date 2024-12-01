import pytest
import requests

BASE_URL = "https://dummyjson.com"

# Testando os endpoints gerais da API
@pytest.mark.parametrize("endpoint", [
    f"{BASE_URL}/products",        # Todos os produtos
    f"{BASE_URL}/users",           # Todos os usuários
    f"{BASE_URL}/products/1",      # Produto específico (ID 1)
    f"{BASE_URL}/users/1",         # Usuário específico (ID 1)
])
def test_api_endpoints(endpoint):
    response = requests.get(endpoint)
    
    # Verificar o status da rota
    assert response.status_code == 200, f"Falha ao acessar a rota: {endpoint} (Status: {response.status_code})"
    # Remover o print para uma saída mais limpa
    # print(f"Teste bem-sucedido para a rota: {endpoint}")
    # print(f"Status da rota: {response.status_code}\n")

# Testando produto por ID
@pytest.mark.parametrize("product_id, expected_name", [
    (1, "Essence Mascara Lash Princess"),  # Nome do produto com ID 1
    (2, "Eyeshadow Palette with Mirror"),  # Nome do produto com ID 2
    (3, "Powder Canister"),   # Nome do produto com ID 3
])
def test_product_by_id(product_id, expected_name):
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    assert response.status_code == 200, f"Falha ao acessar produto com ID {product_id}"
    
    # Verificar o conteúdo da resposta
    data = response.json()
    # Checar se o campo 'title' existe
    assert "title" in data, f"Esperado o campo 'title', mas não encontrado: {data}"
    assert data["title"] == expected_name, f"Esperado: {expected_name}, Recebido: {data['title']}"
    # Adicionar mais verificações, como preço
    assert "price" in data, f"Esperado o campo 'price', mas não encontrado: {data}"

# Testando usuário por ID
@pytest.mark.parametrize("user_id", [
    1, 2, 3  # Testar alguns usuários com IDs conhecidos
])
def test_user_by_id(user_id):
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200, f"Falha ao acessar usuário com ID {user_id}"
    
    data = response.json()
    assert data["id"] == user_id, f"Esperado ID {user_id}, Recebido ID {data['id']}"
    # Adicionar verificações extras sobre o usuário
    assert "username" in data, f"Esperado o campo 'username', mas não encontrado: {data}"
    # print(f"Usuário com ID {user_id}: {data['username']} (Status: {response.status_code})\n")

# Teste 1: Testar endpoint de produtos com sucesso
def test_get_all_products_success():
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200, "Falha ao obter todos os produtos."
    data = response.json()
    assert "products" in data, "A resposta não contém o campo 'products'."
    assert isinstance(data["products"], list), "O campo 'products' não é uma lista."

# Teste 2: Testar endpoint de um produto específico com sucesso
def test_get_product_by_id_success():
    product_id = 1
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    assert response.status_code == 200, f"Falha ao obter produto com ID {product_id}."
    data = response.json()
    assert data["id"] == product_id, f"Esperado ID {product_id}, mas recebido {data['id']}."
    assert "title" in data, "A resposta não contém o campo 'title'."

# Teste 3: Testar erro ao acessar um produto inexistente
def test_get_product_by_invalid_id():
    invalid_id = 9999  # ID que não existe
    response = requests.get(f"{BASE_URL}/products/{invalid_id}")
    assert response.status_code == 404, f"Esperado status 404 para produto com ID {invalid_id}, mas recebido {response.status_code}."
    data = response.json()
    assert "message" in data, "A resposta não contém o campo 'message' para o erro."

# Teste 4: Verificar dados do endpoint de usuários
def test_get_user_by_id_success():
    user_id = 1
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200, f"Falha ao obter usuário com ID {user_id}."
    data = response.json()
    assert data["id"] == user_id, f"Esperado ID {user_id}, mas recebido {data['id']}."
    assert "username" in data, "A resposta não contém o campo 'username'."


