from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def eliminar_fila_por_numero(numero_fila):
    # Construir el XPath para encontrar el botón de eliminar en la fila específica
    delete_button_xpath = f"//tbody[@id='table-body']/tr[{numero_fila}]/td/button[@class='delete-button']"

    # Encontrar y hacer clic en el botón de eliminar en la fila específica
    delete_button = driver.find_element_by_xpath(delete_button_xpath)
    delete_button.click()
    time.sleep(1)  # Esperar un segundo para que la fila se elimine completamente


def anhadir_fila_por_numero(numero_fila):
    # Construir el XPath para encontrar el botón de eliminar en la fila específica
    add_button_xpath = f"//tbody[@id='table-body']/tr[{numero_fila}]/td/button[@class='add-row-button']"

    # Encontrar y hacer clic en el botón de eliminar en la fila específica
    add_button = driver.find_element_by_xpath(add_button_xpath)
    add_button.click()
    time.sleep(1)  # Esperar un segundo para que la fila se elimine completamente


# Inicializar el navegador
driver = webdriver.Chrome()  # Asegúrate de tener el driver de Chrome instalado y en el PATH

try:
    # Abrir la página web
    driver.get("file:///C:/Users/victo/OneDrive/Documentos/TfgColors/web_client/index.html")
    time.sleep(1)

    # Añado una fila
    anhadir_fila_por_numero(1)
    time.sleep(1)

    # modificar material de la fila añadida
    select_xpath = f"//tbody[@id='table-body']/tr[{1}]/td[{2}]/select"
    select_element = driver.find_element_by_xpath(select_xpath)
    select_element.click()  # Hacer clic en el select para abrir las opciones
    time.sleep(1)
    select_element.send_keys("other material")  # Enviar las teclas para escribir "au" y filtrar las opciones
    time.sleep(1)
    select_element.send_keys(Keys.ENTER)
    time.sleep(2)
    thickness_input = driver.find_element_by_xpath("//input[@placeholder='Enter numeric value']")
    thickness_input.send_keys("1")
    time.sleep(1)

    # Modificar el grosor de la fila añadida
    thickness_input = driver.find_element_by_xpath("//tbody[@id='table-body']/tr[2]/td[3]/input")
    thickness_input.clear()
    thickness_input.send_keys("100")
    time.sleep(1)

    # Modificar el grosor de la fila incial
    thickness_input = driver.find_element_by_xpath("//tbody[@id='table-body']/tr[3]/td[3]/input")
    # Suponiendo que el primer campo de entrada en la tabla es el campo de grosor
    thickness_input.clear()  # Limpiar cualquier valor existente en el campo
    thickness_input.send_keys("150")
    time.sleep(5)

    # Añado una fila
    anhadir_fila_por_numero(3)

    time.sleep(3)

    eliminar_fila_por_numero(3)
    time.sleep(1)

    # Simular hacer clic en el botón para obtener el color
    get_color_button = driver.find_element_by_id("mostrar-colores-button")
    get_color_button.click()
    time.sleep(1)  # Esperar un segundo para que se calcule el color

    # Verificar si se muestra el color RGB en el resultado
    resultado_json_div = driver.find_element_by_id("resultado-json")
    assert "RGB" in resultado_json_div.text, "No se mostró el color RGB en el resultado"

    print("Prueba exitosa!")

finally:
    # Cerrar el navegador al finalizar
    driver.quit()
