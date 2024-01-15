// CODIGO QUE SE EJECUTA AL CARGAR LA PAGINA
$(document).ready(function() {

    // Suponemos que el boton de intercorrelacion esta pulsado
    var button1 = document.getElementById("button1");
    button1.classList.remove("bg-info");
    button1.classList.add("bg-light");

    // Add los listeners del clic en botones
    var button1 = document.getElementById("button1");
    var button2 = document.getElementById("button2");
    var button3 = document.getElementById("button3");
    var button4 = document.getElementById("button4");

    button1.addEventListener("click", function() {
        button1.classList.remove("bg-info");
        button1.classList.add("bg-light");
        button2.classList.remove("bg-light");
        button2.classList.add("bg-info");
        button3.classList.remove("bg-light");
        button3.classList.add("bg-info");
        button4.classList.remove("bg-light");
        button4.classList.add("bg-info");

        var img1 = document.getElementById("img1");
        var img2 = document.getElementById("img2");
        var img3 = document.getElementById("img3");
        var img4 = document.getElementById("img4");

        img1.hidden = false;
        img2.hidden = true;
        img3.hidden = true;
        img4.hidden = true;
    });

    button2.addEventListener("click", function() {
        button2.classList.remove("bg-info");
        button2.classList.add("bg-light");
        button1.classList.remove("bg-light");
        button1.classList.add("bg-info");
        button3.classList.remove("bg-light");
        button3.classList.add("bg-info");
        button4.classList.remove("bg-light");
        button4.classList.add("bg-info");

        var img1 = document.getElementById("img1");
        var img2 = document.getElementById("img2");
        var img3 = document.getElementById("img3");
        var img4 = document.getElementById("img4");

        img1.hidden = true;
        img2.hidden = false;
        img3.hidden = true;
        img4.hidden = true;
    });

    button3.addEventListener("click", function() {
        button3.classList.remove("bg-info");
        button3.classList.add("bg-light");
        button2.classList.remove("bg-light");
        button2.classList.add("bg-info");
        button1.classList.remove("bg-light");
        button1.classList.add("bg-info");
        button4.classList.remove("bg-light");
        button4.classList.add("bg-info");

        var img1 = document.getElementById("img1");
        var img2 = document.getElementById("img2");
        var img3 = document.getElementById("img3");
        var img4 = document.getElementById("img4");

        console.log(img3)
        img1.hidden = true;
        img2.hidden = true;
        img3.hidden = false;
        img4.hidden = true;
    });

    button4.addEventListener("click", function() {
        button4.classList.remove("bg-info");
        button4.classList.add("bg-light");
        button2.classList.remove("bg-light");
        button2.classList.add("bg-info");
        button3.classList.remove("bg-light");
        button3.classList.add("bg-info");
        button1.classList.remove("bg-light");
        button1.classList.add("bg-info");

        var img1 = document.getElementById("img1");
        var img2 = document.getElementById("img2");
        var img3 = document.getElementById("img3");
        var img4 = document.getElementById("img4");

        img1.hidden = true;
        img2.hidden = true;
        img3.hidden = true;
        img4.hidden = false;
    });
  });