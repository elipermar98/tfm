
import pandas as pd
import joblib
import json

from sklearn.cluster import DBSCAN
from sklearn.cluster import OPTICS

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder

def get_clusters_count(algorithm):
    
    with open("static/analitics/cluster_siluetes.json", 'r') as file:
        data = json.load(file)

    return data[algorithm]


def get_cluster_statistics_by_column(csv_file):
    # Lee el archivo CSV como un DataFrame
    df = pd.read_csv(csv_file)  # Reemplaza 'archivo.csv' con tu nombre de archivo

    columnas_estadisticas = df.columns[df.columns != 'diabetic_label']

    # Eliminamos outlayers
    df = df.loc[df['cluster_label'] != -1]

    # Agrupar por 'cluster_label' y calcular estadísticas
    grupos = df.groupby('cluster_label')[columnas_estadisticas]

    # Lista para almacenar las estadísticas por cada cluster_label
    estadisticas_lista = []

    # Iterar sobre los grupos y obtener las estadísticas para cada grupo
    for cluster, group_data in grupos:
        stats = group_data.describe().round(2).loc[['min', 'max', 'mean', 'std']].to_dict()
        stats.pop('Unnamed: 0')
        stats.pop('cluster_label')
        estadisticas_lista.append({'cluster_label': cluster, 'stats': stats})

    # Creamos la lista de la tabla
    devolver = []

    for element in estadisticas_lista:
        for stat in element['stats']:
            devolver.append([
                element["cluster_label"],
                stat,
                element["stats"][stat]["min"],
                element["stats"][stat]["max"],
                element["stats"][stat]["mean"],
                element["stats"][stat]["std"]
            ])

    return devolver


def get_cluster_statistics_by_column_categoric(csv_file):
    # Lee el archivo CSV como un DataFrame
    df = pd.read_csv(csv_file)  # Reemplaza 'archivo.csv' con tu nombre de archivo

    columnas_valores = ['HighBP', 'HighChol', 'CholCheck', 'Smoker', 'Stroke', 'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth', 'DiffWalk', 'Sex', 'Education', 'Income']

    # Agrupar por 'cluster_label' y calcular estadísticas
    grupos = df.groupby('cluster_label')[columnas_valores]

    # Lista para almacenar las estadísticas por cada cluster_label
    estadisticas_lista = []

    # Iterar sobre los grupos y obtener las estadísticas para cada grupo
    for cluster, group_data in grupos:
        for columna in columnas_valores:
            valores_distintos = group_data[columna].unique()
            valores_como_string = ', '.join(map(str, valores_distintos))
            estadisticas_lista.append([cluster,columna,valores_como_string])

    return estadisticas_lista


def get_cluster_data(csv_file, cluster):
    df = pd.read_csv(csv_file)

    # Variable que almacena los datos en forma de diccionario
    cluster_data = {}

    # Sacar la pertenencia a las tres categorias del cluster para ese algoritmo
    filtered = df[df['cluster_label'] == int(cluster)]
    diabetic_label_counts = filtered['diabetic_label'].value_counts().reset_index()
    lista_diccionarios = diabetic_label_counts.rename(columns={'index': 'category', 'diabetic_label': 'value'}).to_dict(orient='records')
    for item in lista_diccionarios:
        if item['value'] == 0:
            item['value'] = 'No diabético'
        elif item['value'] == 1:
            item['value'] = 'Prediabético'
        elif item['value'] == 2:
            item['value'] = 'Diabético'

    cluster_data["pertenenica_categorias"] = lista_diccionarios

    # Numero de registros pertenecientes al cluster
    num_registros_cluster = df[df['cluster_label'] == int(cluster)].shape[0]
    cluster_data["num_registros_cluster"] = num_registros_cluster

    # Cargamos las estadisticas del algoritmo
    with open("static/analitics/evaluacion_calidad.json", 'r') as file:
        # Cargar el contenido del archivo JSON como un diccionario
        data = json.load(file)
        
        cluster_data["algorithm_data"] = data[csv_file.split("/")[-1].split(".")[0]]
    
    # Datos generales
    cluster_data["algorithm"] = csv_file.split("/")[-1].split(".")[0]
    cluster_data["cluster"] = cluster
    
    return cluster_data

def predict(csv_file, values):
    # Diccionario con valores del formulario
    values.pop("algorithm")

    # Convertir el diccionario en un DataFrame
    df = pd.DataFrame([values])

    # Cargamos la pipeline
    pipeline_cargada = joblib.load(f'static/trained_models/{csv_file}.joblib')

    # Si es algoritmo numerico se quitan el resto de columnas
    if csv_file in ["kmeans", "kmedoids", "dbscan", "affinitypropagation", "optics"]:

        columnas_deseadas = ['MentHlth', 'PhysHlth', 'BMI']
        df = df.loc[:, columnas_deseadas]

        # Si es DBSCAN u OPTICS hay que reentrenar todo el modelo
        if csv_file == "dbscan" or csv_file == "optics":
            df_training = pd.read_csv("static/datasets/clustering_data_preprocesado_reducido.csv")
            df_training = df_training.loc[:, columnas_deseadas]
            merged_df = pd.concat([df_training, df], ignore_index=True)

            if csv_file == "optics":
                # Pipeline Optics
                optics_pipeline = Pipeline([
                    ('MMS', MinMaxScaler()),
                    ('optics', OPTICS(eps=0.75, min_samples=12)) 
                ])

                labels = optics_pipeline.fit_predict(merged_df)
                return labels[-1]
            else:
                # Pipeline DBScan
                dbscan_pipeline = Pipeline([
                    ('MMS', MinMaxScaler()),
                    ('dbscan', DBSCAN(eps=0.12, min_samples=2)) 
                ])

                labels = dbscan_pipeline.fit_predict(merged_df)
                return labels[-1]
        else:
            prediccion = pipeline_cargada.predict(df)
    else:
        columnas_numericas = ['MentHlth', 'PhysHlth', 'BMI', 'Age']
        columnas_categoricas = ['HighBP', 'HighChol', 'CholCheck', 'Smoker', 'Stroke', 'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth', 'DiffWalk', 'Sex', 'Education', 'Income']


        # Convertir las variables categóricas a códigos numéricos usando LabelEncoder
        label_encoders = {}
        for column in columnas_categoricas:
            label_encoders[column] = LabelEncoder()
            df[column] = pd.Categorical(label_encoders[column].fit_transform(df[column]))

        indices_columnas_categoricas = [df.columns.get_loc(col) for col in columnas_categoricas]
        
        prediccion = pipeline_cargada.predict(df[columnas_numericas + columnas_categoricas].values,
                                                categorical=indices_columnas_categoricas)

    return prediccion[0]