import os

# Espacios de memoria disponibles (inicialmente)
espacios_de_memoria = {
    1: {"tamaño": 1000, "ocupado": False},
    2: {"tamaño": 400, "ocupado": False},
    3: {"tamaño": 1800, "ocupado": False},
    4: {"tamaño": 700, "ocupado": False},
    5: {"tamaño": 900, "ocupado": False},
    6: {"tamaño": 1200, "ocupado": False},
    7: {"tamaño": 2000, "ocupado": False},
}

# Archivos disponibles (inicialmente)
archivos = []


# Función para agregar espacios de memoria
def agregar_espacio():
    tamaño = int(input("Ingrese el tamaño del espacio (kbs): "))
    posicion = input("Ingrese la posición (al inicio o al final): ").lower()

    if posicion == "inicio":
        espacios_de_memoria.update({max(espacios_de_memoria.keys()) + 1: {"tamaño": tamaño, "ocupado": False}})
    elif posicion == "final":
        espacios_de_memoria.update({max(espacios_de_memoria.keys()) + 1: {"tamaño": tamaño, "ocupado": False}})
    else:
        print("Posición no válida. Seleccionando al final por defecto.")


# Función para agregar archivos físicos desde una ruta
def agregar_archivos_fisicos(ruta):
    try:
        if os.path.isdir(ruta):
            archivos_en_ruta = os.listdir(ruta)
            for archivo_nombre in archivos_en_ruta:
                archivo_ruta_completa = os.path.join(ruta, archivo_nombre)
                if os.path.isfile(archivo_ruta_completa):
                    tamaño = os.path.getsize(archivo_ruta_completa) // 1024
                    archivos.append({"nombre": archivo_nombre, "tamaño": tamaño, "peso": 0})
            print(f"Se han agregado {len(archivos_en_ruta)} archivos desde la ruta {ruta}.")
        else:
            print("La ruta proporcionada no es un directorio válido.")
    except Exception as e:
        print(f"Error al agregar archivos desde la ruta {ruta}: {str(e)}")


# Función para agregar archivos virtuales y escribir en "archivos.txt"
def agregar_archivos_virtuales():
    while True:
        nombre = input("Ingrese el nombre del archivo: ")
        tamaño = int(input("Ingrese el tamaño del archivo (kbs): "))
        peso = int(input("Ingrese el peso del archivo: "))
        archivos.append({"nombre": nombre, "tamaño": tamaño, "peso": peso})

        # Escribir en "archivos.txt"
        with open("archivos.txt", "a") as archivo_txt:
            archivo_txt.write(f"{nombre}, {tamaño} kb, {peso} peso\n")

        respuesta = input("¿Desea agregar otro archivo virtual? (s/n): ")
        if respuesta.lower() != 's':
            break


# Funciones de asignación de espacio según algoritmo
def primer_ajuste(archivo):
    for espacio, info in espacios_de_memoria.items():
        if not info["ocupado"] and info["tamaño"] >= archivo["tamaño"]:
            info["ocupado"] = True
            return espacio
    return None


def mejor_ajuste(archivo):
    mejor_espacio = None
    for espacio, info in espacios_de_memoria.items():
        if not info["ocupado"] and info["tamaño"] >= archivo["tamaño"]:
            if mejor_espacio is None or info["tamaño"] < espacios_de_memoria[mejor_espacio]["tamaño"]:
                mejor_espacio = espacio
    if mejor_espacio is not None:
        espacios_de_memoria[mejor_espacio]["ocupado"] = True
    return mejor_espacio


def peor_ajuste(archivo):
    peor_espacio = None
    for espacio, info in espacios_de_memoria.items():
        if not info["ocupado"] and info["tamaño"] >= archivo["tamaño"]:
            if peor_espacio is None or info["tamaño"] > espacios_de_memoria[peor_espacio]["tamaño"]:
                peor_espacio = espacio
    if peor_espacio is not None:
        espacios_de_memoria[peor_espacio]["ocupado"] = True
    return peor_espacio


def siguiente_ajuste(archivo, ultimo_espacio):
    espacios_disponibles = list(espacios_de_memoria.keys())
    if ultimo_espacio is None:
        ultimo_espacio = espacios_disponibles[0]
    else:
        ultimo_espacio_index = espacios_disponibles.index(ultimo_espacio)
        espacios_disponibles = espacios_disponibles[ultimo_espacio_index:] + espacios_disponibles[:ultimo_espacio_index]

    for espacio in espacios_disponibles:
        info = espacios_de_memoria[espacio]
        if not info["ocupado"] and info["tamaño"] >= archivo["tamaño"]:
            info["ocupado"] = True
            return espacio
    return None


def asignar_archivos(algoritmo):
    for archivo in archivos:
        espacio = algoritmo(archivo)
        if espacio is not None:
            print(f"Archivo '{archivo['nombre']}' asignado al espacio {espacio} de {archivo['tamaño']} kb.")
        else:
            print(f"No hay espacio suficiente para el archivo '{archivo['nombre']}' de {archivo['tamaño']} kb.")


# Uso de la función agregar_espacio
while True:
    print("\nEspacios de memoria disponibles:")
    for espacio, info in espacios_de_memoria.items():
        print(f"{espacio}. Tamaño: {info['tamaño']} kbs, Ocupado: {info['ocupado']}")

    print("\nOpciones:")
    print("1. Agregar espacio de memoria")
    print("2. Continuar")

    opcion = input("Seleccione una opción (1/2): ")
    if opcion == "1":
        agregar_espacio()
    elif opcion == "2":
        break

# Uso de las funciones agregar_archivos_fisicos y agregar_archivos_virtuales
while True:
    print("\nOpciones:")
    print("1. Agregar archivos físicos desde una ruta")
    print("2. Agregar archivos virtuales")
    print("3. Continuar")

    opcion = input("Seleccione una opción (1/2/3): ")
    if opcion == "1":
        ruta_directorio = input("Ingrese la ruta del directorio de archivos físicos: ")
        agregar_archivos_fisicos(ruta_directorio)
    elif opcion == "2":
        agregar_archivos_virtuales()
    elif opcion == "3":
        break

# Uso de las funciones de asignación de espacio según el algoritmo seleccionado
while True:
    print("\nAlgoritmos de administración de memoria disponibles:")
    print("1. Primer ajuste")
    print("2. Mejor ajuste")
    print("3. Peor ajuste")
    print("4. Siguiente ajuste")
    print("5. Salir")

    opcion = input("Seleccione un algoritmo (1/2/3/4/5): ")
    if opcion == "5":
        break

    if opcion not in ["1", "2", "3", "4"]:
        print("Opción no válida. Intente nuevamente.")
        continue

    if opcion == "1":
        print("Asignando archivos utilizando el algoritmo de Primer Ajuste:")
        asignar_archivos(primer_ajuste)
    elif opcion == "2":
        print("Asignando archivos utilizando el algoritmo de Mejor Ajuste:")
        asignar_archivos(mejor_ajuste)
    elif opcion == "3":
        print("Asignando archivos utilizando el algoritmo de Peor Ajuste:")
        asignar_archivos(peor_ajuste)
    elif opcion == "4":
        print("Asignando archivos utilizando el algoritmo de Siguiente Ajuste:")
        ultimo_espacio_siguiente_ajuste = None
        asignar_archivos(lambda archivo: siguiente_ajuste(archivo, ultimo_espacio_siguiente_ajuste))
