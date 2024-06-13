
function agregarFilaDebajo(row) {
  const tableBody = document.getElementById('table-body');
  const newRow = document.createElement('tr');

  // Obténgo el número de capa actual
  let layerNumber = 1;
  const currentRow = row;

  // Verifico si la celda de la capa actual contiene un número antes de realizar la suma
  const currentLayerCell = currentRow.querySelector('td:first-child');
  if (currentLayerCell && !isNaN(parseInt(currentLayerCell.textContent))) {
    layerNumber = parseInt(currentLayerCell.textContent)+1;
  }

  // Creo la celda para la columna "Layer"
  const layerCell = document.createElement('td');
  layerCell.textContent = layerNumber;
  newRow.appendChild(layerCell);
  const materialCell = document.createElement('td');
  const materialSelect = document.createElement('select');
  materialCell.appendChild(materialSelect);
  newRow.appendChild(materialCell);

  // Creo la Columna "Thickness" como campo de entrada
  const thicknessCell = document.createElement('td');
  const thicknessInput = document.createElement('input');
  thicknessInput.type = 'text';
  thicknessInput.placeholder = 'input thickness';
  thicknessCell.appendChild(thicknessInput);
  newRow.appendChild(thicknessCell);

  // Creo el boton eliminar //eliminar
  const deleteButton = document.createElement('button');
  deleteButton.className = 'delete-button';
  deleteButton.textContent = '✕';
  deleteButton.onclick = function() {
    eliminarFila(newRow);
  };
  //creo el boton añadir nueva fila
  const addRowButton = document.createElement('button');
  addRowButton.className = 'add-row-button';
  addRowButton.textContent = '+';
  addRowButton.onclick = function() {
    agregarFilaDebajo(newRow);
  };

  // ejecuto las acciones creadas arriba
  const actionsCell = document.createElement('td');
  actionsCell.appendChild(deleteButton);
  actionsCell.appendChild(addRowButton);
  newRow.appendChild(actionsCell);

  // Calculo dónde agregar la nueva fila
  const nextRow = row.nextSibling;
  if (nextRow) {
    tableBody.insertBefore(newRow, nextRow);
  } else {
    tableBody.appendChild(newRow);
  }

  //siempre despues de operar actualizo los numeros y cargo materiales
  actualizarNumerosDeCapa(tableBody, newRow, layerNumber + 1);
  cargarMateriales(materialSelect);

}

function actualizarNumerosDeCapa(tableBody, startingRow) {
  const rowsToUpdate = Array.from(tableBody.children).slice(Array.from(tableBody.children).indexOf(startingRow));
  let startingLayerNumber = parseInt(startingRow.querySelector('td:first-child').textContent);
  //recorro las filas necesarias a partir de la fila añadida y sumo 1 al numero
  for (const rowToUpdate of rowsToUpdate) {
    const layerCell = rowToUpdate.querySelector('td:first-child');
    if (layerCell && !isNaN(parseInt(layerCell.textContent))) {
      layerCell.textContent = startingLayerNumber;
      startingLayerNumber++;
    }
  }
}


function eliminarFila(row) {
  var tableBody = document.getElementById('table-body');
  // Obtengo el número de capa de la fila actual
  var layerNumber = parseInt(row.cells[0].textContent, 10);
  // Verifico que el número de capa es un entero
  if (!isNaN(layerNumber)) {
      // Eliminar la fila
      tableBody.removeChild(row);
      // Actualizo los números de capa de las filas posteriores
      var filasPosteriores = tableBody.getElementsByTagName('tr');
      for (var i = layerNumber; i < filasPosteriores.length; i++) {
          // Obtener el valor actual de la capa
          var currentLayer = filasPosteriores[i].cells[0].textContent;
          // Verifico que el valor actual de la capa sea un entero antes de modificarlo
          if (!isNaN(parseInt(currentLayer, 10))) {
              filasPosteriores[i].cells[0].textContent = i;
          }
      }
  } else {
      alert('No se puede actualizar el número de capa para un valor no numérico.');
  }
}


function cargarMateriales(selectElement) {
  // Realizo la solicitud al servidor
  fetch('http://localhost:5000/materiales/label')
    .then(response => {
      if (!response.ok) {
        throw new Error('No se pudo cargar los materiales');
      }
      return response.json();
    })
    .then(data => {
      selectElement.innerHTML = '';
      // Itero sobre los materiales y agregar cada uno al desplegable
      data.forEach(material => {
        const option = document.createElement('option');
        option.value = material;
        option.textContent = material;
        selectElement.appendChild(option);
      });
    })
    .catch(error => console.error('Error al cargar materiales:', error));
}


function changeInputType(selectElement) {
  const selectedValue = selectElement.value;
  const parentCell = selectElement.parentElement;
  let inputField = parentCell.querySelector('input[type="text"]');
  
  if (selectedValue === 'numeric') {
    // Si se selecciona "Numeric Value", mostrar el campo de entrada de texto
    if (!inputField) {
      inputField = document.createElement('input');
      inputField.type = 'text';
      inputField.placeholder = 'Enter numeric value';
      parentCell.appendChild(inputField);
    }
  } else {
    // Si se selecciona "Air", eliminar el campo de entrada de texto si existe
    if (inputField) {
      parentCell.removeChild(inputField);
    }
  }
}



function obtenerColores() {
  const resultadoJsonDiv = document.getElementById('resultado-json');
  // Obtener todas las filas de la tabla
  const filas = document.querySelectorAll('#table-body tr');
  // Arrays para almacenar materiales y grosores
  const materialesArray = [];
  const grosoresArray = [];
  let hayError = false;
  let mensajeError = '';
  // Obtener el material de la fila
    filas.forEach((fila, index) => {
      if (index === 0) {
        // Si es la primera fila, verificar el campo y agregar a los arrays según corresponda
        const airNumericInput = fila.querySelector('input[type="text"]');
        const airNumericValue = airNumericInput ? airNumericInput.value.trim() : '';
        // Si hay un valor numérico, lo uso; sino, uso 'Air'
        const selectedValue = airNumericValue ? airNumericValue : 'Air'; 
        materialesArray.push(selectedValue);
      } else {
      const materialSelect = fila.querySelector('select');
      // Valor predeterminado 'si' si no se encuentra ningún elemento <select>, utilizado inicialmente para la última fila
      const materialSeleccionado = materialSelect ? materialSelect.value : 'si'; 
      materialesArray.push(materialSeleccionado);
      }
    });
    //Comprobacion de que se exige al menos una capa distinta del aire y el sustrato
    if (materialesArray.length === 2) {
      hayError = true;
      mensajeError = 'You should add at least one layer.';
    }
  // Itero sobre todas las filas de la tabla para procesar el grosor, excepto la primera y la última fila
  for (let i = 1; i < filas.length-1; i++) {
      const fila = filas[i];
      // Obtener el grosor de la fila
      const grosorInput = fila.querySelector('input[type="text"]');
      //sino tiene grosor pongo 20 por defecto
      const grosorIngresado = grosorInput ? (grosorInput.value.trim() === '' ? 20 : grosorInput.value) : 20;
      //control de errores
      if (isNaN(grosorIngresado)){
        hayError = true;
        mensajeError = 'Thikness field must be a numeric value';
        break; 
      }
      if (parseFloat(grosorIngresado) <= 0) {
        hayError = true;
        mensajeError = 'Thikness value must be a number greater than 0';
        break;
      }
      grosoresArray.push(grosorIngresado);
     }
     //caso de error
    if (hayError) {
    resultadoJsonDiv.textContent = mensajeError;
    return; 
  }

  // Hago la solicitud al servidor con los valores obtenidos
  fetch(`http://localhost:5000/colors/${materialesArray.join(',')}/${grosoresArray.join(',')}`)
    .then(response => {
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Error server not found');
        } else if (response.status === 500) {
          throw new Error('Internal server error');
        } else {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
      }
      return response.json();
    })

  .then(data => {
    let formattedResult = ''; 

    let rgbValue = '';

    for (const key in data) {
      // Reemplazo "rgb" por "RGB" en el nombre de la propiedad
      const propertyName = key.toLowerCase() === 'rgb' ? 'RGB' : key;

      if (propertyName.toLowerCase() === 'rgb') {
        rgbValue = `{${data[key].join(',')}}`;
      } else {
       formattedResult += `"${propertyName}": ${data[key]}, `;
      }
    }

    formattedResult = `RGB: ${rgbValue}`;
    // Muestro los datos en formato personalizado en la interfaz
    resultadoJsonDiv.textContent = formattedResult;
    const rgbValues = data.rgb;
    mostrarColorRGB(rgbValues);
  })
  .catch(error => {
      console.error('Error retrieving colors:', error);
      // Manejar el error si es necesario
      if (error.message.includes('Server not found')) {
        resultadoJsonDiv.textContent = 'Error: Server not found.';
      } else if (error.message.includes('Internal server error')) {
        resultadoJsonDiv.textContent = 'Error: Internal server error';
      } else {
        resultadoJsonDiv.textContent = 'Error: Unable to connect to the server.';
      }   
    });
}

function mostrarColorRGB(rgb) {
  // Obtengo el elemento div donde se mostrará el color
  const colorDiv = document.getElementById('color-div');
  // Verifico si el elemento div existe
  if (colorDiv) {
    // Crear una cadena de estilo CSS con las coordenadas RGB
    const colorStyle = `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
    // Establecer el color de fondo del div
    colorDiv.style.backgroundColor = colorStyle;
  } else {
    console.error('Elemento div no encontrado.');
  }
}

// Ejecuto la función al cargar la página o en algún evento
document.addEventListener('DOMContentLoaded', function() {
  const addButton = document.getElementById('add-row-button');
  const mostrarColoresButton = document.getElementById('mostrar-colores-button');
  const firstSelect = document.getElementById('materiales');
  const secondSelect = document.getElementById('sustratos');
  if (addButton) {
    addButton.onclick = function() {
    const tableBody = document.getElementById('table-body');
    const firstRow = tableBody.children[0];
    agregarFilaDebajo(firstRow);
  
    }
  
  };
  //operaciones siempre requeridas
  cargarMateriales(firstSelect);
  cargarMateriales(secondSelect);
  mostrarColoresButton.onclick = obtenerColores;
});

