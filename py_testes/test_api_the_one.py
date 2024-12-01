import pytest
import requests

# BASE URL da The One API e chave de acesso
BASE_URL = "https://the-one-api.dev/v2"
API_KEY = "O81YPv3jVyOW_PmZKQj7"  # Chave de Acesso da API

# Configurações de cabeçalhos
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def test_get_movies():
    # Testa a recuperação da lista de filmes
    endpoint = "/movie"
    response = requests.get(BASE_URL + endpoint, headers=HEADERS)
    assert response.status_code == 200, "Erro ao acessar API"
    data = response.json()
    assert len(data["docs"]) > 0, "Nenhum filme foi retornado"
    print(f"Filmes retornados: {len(data['docs'])}")


def test_get_specific_movie():
    # Recupera todos os filmes e encontra o ID correto para "The Fellowship of the Ring"
    movies_response = requests.get(BASE_URL + "/movie", headers=HEADERS)
    assert movies_response.status_code == 200, "Erro ao acessar API"
    movies_data = movies_response.json()
    
    # Procura o ID do filme "The Fellowship of the Ring"
    fellowship_movie = next(
        (movie for movie in movies_data["docs"] if movie["name"] == "The Fellowship of the Ring"),
        None
    )
    assert fellowship_movie, "O filme 'The Fellowship of the Ring' não foi encontrado"
    movie_id = fellowship_movie["_id"]

    # Testa o endpoint do filme com o ID recuperado
    endpoint = f"/movie/{movie_id}"
    response = requests.get(BASE_URL + endpoint, headers=HEADERS)
    assert response.status_code == 200, "Erro ao acessar API"
    data = response.json()
    assert data["docs"][0]["name"] == "The Fellowship of the Ring", f"Filme incorreto: {data['docs'][0]['name']}"
    print(f"Filme retornado: {data['docs'][0]['name']}")


def test_get_movie_quotes():
    # Testa a recuperação de citações de um filme específico
    movie_id = "5cd95395de30eff6ebccde5d"  # ID do filme "The Fellowship of the Ring"
    endpoint = f"/movie/{movie_id}/quote"
    response = requests.get(BASE_URL + endpoint, headers=HEADERS)
    assert response.status_code == 200, "Erro ao acessar API"
    data = response.json()
    assert len(data["docs"]) > 0, "Nenhuma citação foi retornada"
    print(f"Citações retornadas: {len(data['docs'])}")


def test_get_characters():
    # Testa a recuperação da lista de personagens
    endpoint = "/character"
    response = requests.get(BASE_URL + endpoint, headers=HEADERS)
    assert response.status_code == 200, "Erro ao acessar API"
    data = response.json()
    assert len(data["docs"]) > 0, "Nenhum personagem foi retornado"
    print(f"Personagens retornados: {len(data['docs'])}")


@pytest.mark.parametrize("character_name, expected_name", [
    ("Frodo Baggins", "Frodo Baggins"),    # Caso de sucesso para Frodo
    ("Gandalf", "Gandalf"),                # Caso de sucesso para Gandalf
    ("Aragorn II Elessar", "Aragorn II Elessar"),  # Nome completo de Aragorn
    ("Legolas", "Legolas"),               # Caso de sucesso para Legolas
    ("Nonexistent", None),                # Caso para personagem inexistente
])
def test_search_character_parametrized(character_name, expected_name):
    # Testa a busca de personagens por nome usando parâmetros
    endpoint = "/character"
    params = {"name": character_name}
    response = requests.get(BASE_URL + endpoint, headers=HEADERS, params=params)
    assert response.status_code == 200, f"Erro ao acessar API para {character_name}"
    data = response.json()

    # Log para depuração
    print(f"Consulta: {character_name} | Resposta: {data}")

    if expected_name:
        # Caso esperado: personagem encontrado
        assert len(data["docs"]) > 0, f"Nenhum personagem encontrado para {character_name}"
        assert data["docs"][0]["name"] == expected_name, f"Esperado: {expected_name}, Recebido: {data['docs'][0]['name']}"
        print(f"Personagem encontrado: {data['docs'][0]['name']}")
    else:
        # Caso esperado: nenhum personagem encontrado
        assert len(data["docs"]) == 0, f"Personagem inesperado encontrado para {character_name}"



