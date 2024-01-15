"""
Elisa Perez Martin
TFM - Master Bioinformatica
© GNU Free Documentation License
"""
import csv

import pandas as pd

from flask import Flask, render_template, request
from scripts.csv_analysis import analizar_columnas_csv
from scripts.cluster_info import get_clusters_count,get_cluster_statistics_by_column, get_cluster_data, predict, get_cluster_statistics_by_column_categoric

# Setea a modo debug la app de flask
DEVELOPMENT_ENV = True

app = Flask(__name__)

app_data = {
    "name": "Analisis accesible de grupos y caracteristicas en Datos de Potenciales Pacientes de Diables utilizando técnicas de aprendizaje no supervisado.",
    "description": "Web para dotar de accesibilidad al proyecto de TFM",
    "author": "Elisa Perez Martin",
    "html_title": "TFM Elisa Perez",
    "project_name": "TFM",
    "keywords": "flask, webapp, ml, clustering",
}


#####################################################
#                  RUTAS DE LA WEB                  #
#####################################################
@app.route("/")
def index():
    return render_template("about.html", app_data=app_data)

@app.route("/dataset")
def dataset():
    return render_template("dataset.html", app_data=app_data)

@app.route("/clusters")
def clusters():
    return render_template("clusters.html", app_data=app_data)

@app.route("/clusters_categoric")
def clusters_categoric():
    return render_template("clusters_categoric.html", app_data=app_data)

@app.route("/cluster_info")
def cluster_info():
    return render_template("cluster.html", app_data=app_data)

@app.route("/make_cluster")
def make_cluster():
    return render_template("make_cluster.html", app_data=app_data)

@app.route("/about")
def about():
    return render_template("about.html", app_data=app_data)


#####################################################
#                      DATASETS                     #
#####################################################
@app.route('/csv_train_columns', methods=['POST'])
def csv_train_columns():
    # Devolvemos los nombres de las columnas como respuesta en formato JSON
    return analizar_columnas_csv('static/datasets/clustering_data_preprocesado_reducido.csv')


#####################################################
#                      CLUSTERS                     #
#####################################################
@app.route('/clusters_count', methods=['POST'])
def clusters_count():
    data = request.json
    algorithm_value = data.get('algorithm')
    return {"data": get_clusters_count(algorithm_value)}

@app.route('/cluster_data', methods=['POST'])
def cluster_data():
    data = request.json
    algorithm_value = data.get('algorithm')
    cluster = data.get('cluster')
    return {"data": get_cluster_data(f'static/datasets/{algorithm_value}.csv', cluster)}

@app.route('/algorithm_table', methods=['POST'])
def algorithm_table():
    data = request.json
    algorithm_value = data.get('algorithm')
    return {"data": get_cluster_statistics_by_column(f'static/datasets/{algorithm_value}.csv')}

@app.route('/algorithm_table_categoric', methods=['POST'])
def algorithm_table_categoric():
    data = request.json
    algorithm_value = data.get('algorithm')
    return {"data": get_cluster_statistics_by_column_categoric(f'static/datasets/{algorithm_value}.csv')}

@app.route('/make_cluster_algorithm', methods=['POST'])
def make_cluster_algorithm():
    data = request.json
    algorithm_value = data.get('algorithm')
    cluster = predict(algorithm_value,data)
    return {"cluster": int(cluster)}


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=DEVELOPMENT_ENV)