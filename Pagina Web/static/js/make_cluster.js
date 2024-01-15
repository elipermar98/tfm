// CODIGO QUE SE EJECUTA AL CARGAR LA PAGINA
$(document).ready(function() {
    $('#miFormulario').submit(function(event) {
        event.preventDefault(); // Evita el envío del formulario por defecto

        // Obtiene los datos del formulario
        const formData = new FormData(this);
        const formValues = {};

        // Recorre los datos del formulario y los agrega al objeto formValues
        for (let [key, value] of formData.entries()) {
            formValues[key] = value;
        }

        $.ajax({
            type: 'POST',
            url: '/make_cluster_algorithm', 
            contentType: 'application/json',
            data: JSON.stringify(formValues),
            success: function(data) {
              cluster = data["cluster"]
              algorithm = formValues["algorithm"]

              let url = `/cluster_info?cluster=${cluster}&algorithm=${algorithm}`;

            // Redireccionar a una nueva pestaña con la URL que contiene los parámetros
            window.location.href = url;
              
            },
            error: function(xhr, status, error) {
              console.error('Error al obtener los datos:', error);
            }
        });
    });
});