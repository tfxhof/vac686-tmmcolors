from src.lee_fichero import leer_fichero


def saludar(nombre):
    """Función que saluda a una persona."""
    print(f"Hol {nombre}!")


def main():
    """Función principal del programa."""
    print("¡Bienvenido al programa!")

    # Solicitar al usuario que ingrese su nombre
    nombre = leer_fichero("si")

    # Llamar a la función para saludar
    saludar(nombre)

    print("¡Gracias por usar este programa!")


# Verificar si este script se está ejecutando directamente
if __name__ == "__main__":
    # Llamar a la función principal
    main()
