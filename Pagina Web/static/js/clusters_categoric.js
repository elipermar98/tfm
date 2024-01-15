// CODIGO QUE SE EJECUTA AL CARGAR LA PAGINA
$(document).ready(function() {

    // Filtro de la tabla
    $('#valueFilter').on('keyup', function () {
        const column = parseInt($('#columnFilter').val());
        const value = $(this).val().toLowerCase();
        $('#myTable tbody tr').filter(function () {
          const text = $(this).find('td').eq(column).text().toLowerCase();
          $(this).toggle(text.indexOf(value) > -1);
        });
    });

    // Suponemos que el boton de intercorrelacion esta pulsado
    var button1 = document.getElementById("cluster1");
    button1.classList.remove("bg-info");
    button1.classList.add("bg-light");
    
    // Tabla inicial
    get_table_data("kprototypes");

    // Amcharts inicial
    const data = get_chart_data("kprototypes");

    // Crear la instancia del gráfico de barras
    window.chart = am4core.create('chartDiv', am4charts.XYChart);

    // Configurar datos para la gráfica
    window.chart.data = data;

    // Configurar ejes y series
    let categoryAxis = window.chart.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = 'category';

    let valueAxis = window.chart.yAxes.push(new am4charts.ValueAxis());

    let series = window.chart.series.push(new am4charts.ColumnSeries());
    series.dataFields.valueY = 'value';
    series.dataFields.categoryX = 'category';
    series.name = 'Valor';
    series.columns.template.tooltipText = '{categoryX}: [bold]{valueY}[/]';
});

function get_chart_data(algorithmValue) {
    // Cuerpo de la solicitud
    const requestBody = {
      algorithm: algorithmValue
    };
  
    // Realizar la solicitud al endpoint con AJAX
    $.ajax({
      type: 'POST',
      url: '/clusters_count', 
      contentType: 'application/json',
      data: JSON.stringify(requestBody),
      success: function(data) {
        // Suponiendo que "chart" es tu gráfico de AmCharts
        window.chart.data = data["data"]; // Actualiza los datos del gráfico
        window.chart.validateData(); // Valida y actualiza el gráfico
      },
      error: function(xhr, status, error) {
        console.error('Error al obtener los datos:', error);
      }
    });
}


function get_table_data(algorithmValue) {
    // Cuerpo de la solicitud
    const requestBody = {
        algorithm: algorithmValue
      };
    
    document.getElementById('myTable').querySelector('tbody').innerHTML = '';

      // Realizar la solicitud al endpoint con AJAX
    $.ajax({
        type: 'POST',
        url: '/algorithm_table_categoric', // Reemplaza con la URL correcta de tu endpoint
        contentType: 'application/json',
        data: JSON.stringify(requestBody),
        success: function(data) {
          rows_data = data["data"]; // Actualiza los datos del gráfico
          const tabla = document.getElementById('myTable');
          const cuerpoTabla = tabla.querySelector('tbody');
        
          console.log(rows_data)
      
          // Cargar filas en el cuerpo de la tabla
          for (let i = 0; i < rows_data.length; i++) {
            const fila = document.createElement('tr');
            for (let j = 0; j < rows_data[i].length; j++) {
              const celda = document.createElement('td');
              celda.textContent = rows_data[i][j];
              fila.appendChild(celda);
            }

            // Agregar botón con enlace a /cluster_info?cluster=1 (o número de cluster correspondiente)
            const celda = document.createElement('td');
            const boton = document.createElement('button');
            boton.classList.add('btn', 'btn-info'); 
            const link = document.createElement('a');
            boton.textContent = '>';
            link.href = `/cluster_info?cluster=${rows_data[i][0]}&algorithm=${algorithmValue}`;
            link.appendChild(boton);
            celda.appendChild(link);
            fila.appendChild(celda);

            cuerpoTabla.appendChild(fila);
          }
        },
        error: function(xhr, status, error) {
          console.error('Error al obtener los datos:', error);
        }
      });
}