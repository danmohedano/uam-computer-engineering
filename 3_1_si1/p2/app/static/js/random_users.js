var interval;
var direction; 

function generar_usuarios(dir){
    direction = dir;
    interval = setInterval(generar, 3000);
}

function generar(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (xhttp.readyState == 4 && xhttp.status == 200){
            document.getElementById("usuarios-conectados").innerHTML = xhttp.responseText;
        }
    }

    xhttp.open("GET", direction, true);
    xhttp.send();
}

