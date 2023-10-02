$(document).ready(function () {

    var uri = "";
    var pulpa = "";

    $.ajax({
        url: '/fredy',
        data: { 'parametro': uri },
        type: 'POST',
        success: function(response){
            pulpa = response;
            descripcion(pulpa);
            console.log(response);
        },
        error: function(error){
            console.log(error);
        }
    });


    $("#haha").click(function () {
        window.location.href = "/imagenes";
    });

    nombre = "Melanie";

    function descripcion(pulpa) {
        var arreglo = pulpa.split("@");

        $("#av1").text(arreglo[0]);
        $("#av2").text(arreglo[1]);
        $("#av3").text(arreglo[2]);
        $("#av4").text(arreglo[3]);
    }

    


    $(".tlayuda").hover(function(){
        $(this).removeClass("");
        $(this).addClass(" big");
        }, function(){
        $(this).removeClass("big");
        $(this).addClass("");
    });

    $(".logo").click(function () {
        window.location.href = "/esperanza";
    });

    $(".menu2").hover(function(){
        $(this).removeClass("bg-dark");
        $(this).addClass("bg-secondary shrink");
        }, function(){
        $(this).removeClass("bg-secondary shrink");
        $(this).addClass("bg-dark");
    });

});


