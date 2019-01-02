window.onload = function () {


getData();
stringResult(valor);
console.log(tiempos);

var minimo = Math.min(...tiempo_noZero);
var maximo = Math.max(...tiempos);
var promedio = average(tiempo_noZero);
promedio = promedio.toFixed(2);

document.getElementById("minimo_value").innerHTML = minimo + ' milisegundos';
document.getElementById("maximo_value").innerHTML = maximo + ' milisegundos';
document.getElementById("average_value").innerHTML = promedio + ' milisegundos';
document.getElementById("hit_value").innerHTML = acierto;
document.getElementById("fail_value").innerHTML = fallo;
document.getElementById("error_value").innerHTML = error;

}

function getData(){
    var session = document.getElementById("session_data").textContent;
    var session_decode = JSON.parse(session);
    var id = session_decode.id;
    console.log(id);
    document.getElementById('session_id').value = id;
    var session_results = JSON.parse(session_decode.results);
    var no = session_results.numero;
    var tiempos_str = session_results.tiempos;
    valor = session_results.resultado;
    numero = toInt_value(no);
    tiempos = toInt_value(tiempos_str);
    tiempo_noZero = noZeroTime(tiempos);
}

function toInt_value(array){
    var arreglo = [];
    for (i=1; i < array.length; i++){
        if (isNaN(array[i]) === true){
            arreglo.push(0);
        }
        else{
            arreglo.push(parseInt(array[i])); 
        } 
    }
    return arreglo;
}

function noZeroTime(array){
    var noZeroTime = [];
    for (let i = 0; i < array.length; i++) {
        if(array[i] > 0){
            noZeroTime.push(array[i]);
        }
    }
    return noZeroTime;
}


function stringResult(array){
    acierto = 0;
    fallo = 0;
    error = 0;
    for (i=1; i < array.length; i++){
        if(array[i] === "Hit"){
            acierto++;
        }
        if(array[i] === "Miss"){
            fallo++;
        }
        if(array[i] === "Error"){
            error++;
        }

    }
}

function average(array) {
    var  suma = 0;
    var no = array.length;
    for (i = 0; i < array.length; i++) {
        suma = suma + array[i];     
    }
    return promedio = suma/no;   
}

function postResults() {
    document.getElementById("detailResults").submit();
  }