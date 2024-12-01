from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

def test_youtube_search():
    # Configurar o driver
    driver = webdriver.Chrome()  # Substitua por webdriver.Firefox() se estiver usando o Firefox
    driver.maximize_window()

    try:
        # Abrir o YouTube
        driver.get("https://www.youtube.com")
        time.sleep(3)  # Esperar o carregamento da página

        # Localizar a barra de pesquisa
        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys("Curso Selenium")
        search_box.send_keys(Keys.RETURN)  # Pressionar Enter para buscar

        time.sleep(5)  # Esperar os resultados carregarem

        # Obter a lista de vídeos nos resultados
        results = driver.find_elements(By.ID, "video-title")

        # Certificar que existem resultados e clicar no primeiro vídeo
        if results:
            print(f"Vídeo encontrado: {results[0].text}")
            ActionChains(driver).move_to_element(results[0]).click(results[0]).perform()
        else:
            raise Exception("Nenhum vídeo encontrado para 'Curso Selenium'.")

        # Aguardar o carregamento do vídeo
        time.sleep(10)  # Ajuste conforme necessário para testes manuais

    except Exception as e:
        print(f"Erro durante o teste: {e}")

    finally:
        # Fechar o navegador
        driver.quit()

# Executar a função de teste
test_youtube_search()

