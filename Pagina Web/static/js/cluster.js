// CODIGO QUE SE EJECUTA AL CARGAR LA PAGINA
$(document).ready(function() {
    // Obtener la cadena de consulta (?dato1=valor1&dato2=valor2)
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const cluster = urlParams.get('cluster');
    const algorithm = urlParams.get('algorithm');

    // Cuerpo de la solicitud
    const requestBody = {
        algorithm: algorithm,
        cluster: cluster
    };
  
      
    $.ajax({
        type: 'POST',
        url: '/cluster_data', 
        contentType: 'application/json',
        data: JSON.stringify(requestBody),
        success: function(data) {
          data = data["data"]
          // Función para cargar los datos en los elementos <span>
          function cargarDatos() {
            document.getElementById('num_registros_cluster').innerText = data['num_registros_cluster'];

            document.getElementById('silueta').innerText = data['algorithm_data']['silueta'];
            document.getElementById('davies_bouldin').innerText = data['algorithm_data']['davies_bouldin'];

            document.getElementById('algorithm').innerText = data['algorithm'];
            document.getElementById('cluster').innerText = data['cluster'];
          }

          // Llamar a la función para cargar los datos
          cargarDatos();

          // Amcharts inicial
          const chat_data = data["pertenenica_categorias"]

          // Crear la instancia del gráfico de barras
          window.chart = am4core.create('chartdiv', am4charts.XYChart);

          // Configurar datos para la gráfica
          window.chart.data = chat_data;

          // Configurar ejes y series
          let categoryAxis = window.chart.xAxes.push(new am4charts.CategoryAxis());
          categoryAxis.dataFields.category = 'value';

          let valueAxis = window.chart.yAxes.push(new am4charts.ValueAxis());

          let series = window.chart.series.push(new am4charts.ColumnSeries());
          series.dataFields.valueY = 'count';
          series.dataFields.categoryX = 'value';
          series.name = 'Valor';
          series.columns.template.tooltipText = '{categoryX}: [bold]{valueY}[/]';
        },
        error: function(xhr, status, error) {
          console.error('Error al obtener los datos:', error);
        }
    });
});