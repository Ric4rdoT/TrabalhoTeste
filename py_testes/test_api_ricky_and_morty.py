import pytest
import requests

#Executar Teste: pytest
#Executar Testes e obter também Respostas de rotas: pytest -s py-simulator/test_api_rickyMorty.py


BASE_URL = "https://rickandmortyapi.com/api"

@pytest.mark.parametrize("endpoint", [
    f"{BASE_URL}/character",         # Todos os personagens
    f"{BASE_URL}/location",          # Todas as localizações
    f"{BASE_URL}/episode",           # Todos os episódios
    f"{BASE_URL}/character/1",       # Personagem específico (Rick Sanchez)
    f"{BASE_URL}/episode/1",         # Episódio específico (Pilot)
])
def test_api_endpoints(endpoint):
    response = requests.get(endpoint)
    
    # Verificar o status da rota
    assert response.status_code == 200, f"Falha ao acessar a rota: {endpoint} (Status: {response.status_code})"
    print(f"Teste bem-sucedido para a rota: {endpoint}")
    print(f"Status da rota: {response.status_code}\n")

@pytest.mark.parametrize("character_id, expected_name", [
    (1, "Rick Sanchez"),  # Verificar se o ID 1 retorna "Rick Sanchez"
    (2, "Morty Smith"),   # Verificar se o ID 2 retorna "Morty Smith"
    (3, "Summer Smith"),  # Verificar se o ID 3 retorna "Summer Smith"
    (4, "Beth Smith"),    # Verificar se o ID 4 retorna "Beth Smith"
    (5, "Jerry Smith"),   # Verificar se o ID 5 retorna "Jerry Smith"
])
def test_character_by_id(character_id, expected_name):
    response = requests.get(f"{BASE_URL}/character/{character_id}")
    assert response.status_code == 200, f"Falha ao acessar personagem ID {character_id}"
    data = response.json()
    assert data["name"] == expected_name, f"Esperado: {expected_name}, Recebido: {data['name']}"
    print(f"Personagem com ID {character_id}: {data['name']} (Status: {response.status_code})\n")

def test_filter_characters_by_status():
    # Teste para buscar personagens vivos
    response = requests.get(f"{BASE_URL}/character/?status=alive")
    assert response.status_code == 200, "Erro ao filtrar personagens vivos"
    data = response.json()
    assert "results" in data and len(data["results"]) > 0, "Nenhum personagem vivo encontrado"
    print(f"Personagens vivos encontrados: {len(data['results'])} (Status: {response.status_code})\n")

def test_filter_locations_by_dimension():
    # Teste para buscar localizações em uma dimensão específica
    dimension = "Dimension C-137"
    response = requests.get(f"{BASE_URL}/location/?dimension={dimension}")
    assert response.status_code == 200, f"Erro ao buscar dimensões: {dimension}"
    data = response.json()
    assert "results" in data and len(data["results"]) > 0, f"Nenhuma localização encontrada para {dimension}"
    print(f"Localizações na dimensão {dimension}: {len(data['results'])} (Status: {response.status_code})\n")

def test_episode_name_by_id():
    # Teste para verificar o nome de um episódio específico
    episode_id = 1
    response = requests.get(f"{BASE_URL}/episode/{episode_id}")
    assert response.status_code == 200, f"Erro ao buscar episódio com ID {episode_id}"
    data = response.json()
    assert data["name"] == "Pilot", f"Esperado: Pilot, Recebido: {data['name']}"
    print(f"Episódio com ID {episode_id}: {data['name']} (Status: {response.status_code})\n")



