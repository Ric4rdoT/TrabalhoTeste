import pytest
import requests

# BASE URL da API Deck of Cards
BASE_URL = "https://deckofcardsapi.com/api/deck"

def test_create_new_deck():
    # Testa a criação de um novo baralho
    response = requests.get(f"{BASE_URL}/new/")
    assert response.status_code == 200, "Erro ao acessar API"
    data = response.json()
    assert data["success"], "Erro ao criar novo baralho"
    assert "deck_id" in data, "O ID do baralho não foi retornado"
    print(f"Novo baralho criado com ID: {data['deck_id']}")

def test_draw_cards():
    # Testa o saque de cartas de um novo baralho
    response = requests.get(f"{BASE_URL}/new/draw/?count=2")
    assert response.status_code == 200, "Erro ao acessar API"
    data = response.json()
    assert data["success"], "Erro ao sacar cartas"
    assert len(data["cards"]) == 2, f"Número incorreto de cartas retornadas: {len(data['cards'])}"
    print(f"Cartas sacadas: {[card['code'] for card in data['cards']]}")

def test_reshuffle_deck():
    # Testa o reembaralhamento de um baralho
    # Primeiro cria um novo baralho
    new_deck_response = requests.get(f"{BASE_URL}/new/")
    new_deck_data = new_deck_response.json()
    deck_id = new_deck_data["deck_id"]

    # Reembaralha o baralho
    response = requests.get(f"{BASE_URL}/{deck_id}/shuffle/")
    assert response.status_code == 200, "Erro ao acessar API"
    data = response.json()
    assert data["success"], "Erro ao reembaralhar o baralho"
    assert data["deck_id"] == deck_id, "O ID do baralho mudou após o reembaralhamento"
    print(f"Baralho {deck_id} reembaralhado com sucesso")

def test_partial_deck():
    # Testa a criação de um baralho parcial com cartas específicas
    cards = "AS,2S,3S,4S,5S"
    response = requests.get(f"{BASE_URL}/new/shuffle/?cards={cards}")
    assert response.status_code == 200, "Erro ao acessar API"
    data = response.json()
    assert data["success"], "Erro ao criar baralho parcial"
    assert data["remaining"] == 5, "Número incorreto de cartas restantes no baralho parcial"
    print(f"Baralho parcial criado com as cartas: {cards}")

def test_invalid_draw():
    # Testa o saque de mais cartas do que existem no baralho
    response = requests.get(f"{BASE_URL}/new/draw/?count=60")
    assert response.status_code == 200, "Erro ao acessar API"
    data = response.json()
    assert not data["success"], "O saque deveria falhar"
    assert "error" in data, "Erro não retornado ao tentar sacar mais cartas do que disponíveis"
    print(f"Erro esperado: {data['error']}")
