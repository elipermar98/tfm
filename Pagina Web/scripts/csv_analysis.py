import pandas as pd
import csv

def analizar_columnas_csv(ruta_csv):
    try:
        # Cargar el archivo CSV usando pandas
        data = pd.read_csv(ruta_csv)

        # Crear un diccionario para almacenar la información sobre si las columnas son continuas o no
        columnas_info = {}

        # Iterar sobre las columnas del DataFrame para determinar si son continuas
        for columna in data.columns:
            es_continua = len(data[columna]) >= 2 and sorted(data[columna]) in list(range(1, 11))
            columnas_info[columna] = {}
            columnas_info[columna]["discreta"] = True if es_continua else False
            columnas_info[columna]["values"] = data[columna].unique().tolist() if es_continua else []

        return columnas_info

    except Exception as e:
        # Manejo de errores, por ejemplo, si el archivo no se puede cargar
        return {"error": str(e)}

def nombres_columnas_csv(ruta_csv):
    with open(ruta_csv, newline='') as file:
        csv_reader = csv.reader(file)
        # Leemos la primera fila del archivo CSV 
        column_names = next(csv_reader)

    # Devolvemos los nombres de las columnas como respuesta en formato JSON
    return {"column_names": column_names}