# Refective  RGB color calculation.

---

## Metadatos TfxHoF

- Autor: [Víctor Argüeso Cano](https://www.linkedin.com/in/victor-argueso-cano-28790a273/)
- Título: [API REST y herramienta web para el cálculo del color en materiales multi-capa](https://repositorio.unican.es/xmlui/handle/10902/33693)
- Fecha: Junio 2024

---

## 1. Requirements
- colorpy==0.1.1,
- flask-restx==1.0.3,
- Flask-Cors, Flask,
- mypy-extensions==0.4.3,
- matplotlib, numpy,
- pandas, json5,
- tmm==0.1.8 &
- selenium.

## 3. Project structure
Regarding the project structure, within the `tfgColors` folder there are two folders, `api_color` and `web_client`.

### Server structure.
In the `api_color` folder, the server is created. Within the src directory, there are several folders: the `calculo_color` folder contains the classes with the server's internal logic, and the `rest` folder contains the API that launches the server. Additionally, there is a `test` folder where the unit tests using unittest and the interface tests using Selenium are located. All the server-side code is written in the Python programming language

### Client structure.
In the `web_client` folder, there are three files responsible for generating the client. The `index.html` file contains the HTML code for creating the client's web page. The       `script.js` file contains the client's functionality in JavaScript, and the `style.css` file contains the styling for the client's web page.

## 4.Usage
To run the application, you need to start the server using `api.py`, and then open `index.html` in a web browser.
