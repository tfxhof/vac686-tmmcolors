from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Inicializar el navegador
driver = webdriver.Chrome()  # Asegúrate de tener el driver de Chrome instalado y en el PATH

try:
    # Abrir la página web
    driver.get("file:///C:/Users/victo/OneDrive/Documentos/TfgColors/web_client/index.html")
    time.sleep(5)
    # Simular la interacción del usuario: agregar una nueva fila
    add_row_button = driver.find_element_by_class_name("add-row-button")
    add_row_button.click()
    time.sleep(2)  # Esperar un segundo para que la fila se agregue

    # Obtener los elementos de selección de materiales
    material_selects = driver.find_elements_by_class_name("material-select")

    # Seleccionar el material en el primer select
    material_selects[0].click()
    time.sleep(2)
    material_selects[0].send_keys("au")
    material_selects[0].send_keys(Keys.ENTER)
    time.sleep(2)

    # Simular la entrada de grosor en el primer campo de entrada
    thickness_input = driver.find_element_by_xpath("//input[@placeholder='input thickness']")
    thickness_input.send_keys("100")
    time.sleep(2)

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
