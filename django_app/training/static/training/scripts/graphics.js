window.onload = function () {

var resultTimes = document.getElementById('chartContainer');
getData();
var puntos = formatData(numero,tiempos);
var max = Math.max(...numero);


var chart = new CanvasJS.Chart(resultTimes, {
    animationEnabled: true,
    zoomEnabled: true,
    title:{
        text: "Tiempos de Reacción"
    },
    axisX: {
        title:"Intento",
        minimum: 0,
        maximum: max+1,
    },
    axisY:{
        title: "Tiempo (en ms.)",
        valueFormatString: "##0"
    },
    data: [{
        type: "scatter",
        toolTipContent: "<b>Intento: </b>{x}<br/><b>Tiempo: </b>{y} ms.",
        dataPoints: puntos
    }]
});
chart.render();
}



function getData(){
    var session = document.getElementById("session_data").textContent;
    var session_decode = JSON.parse(session);
    var session_results = JSON.parse(session_decode.results);
    var no = session_results.numero;
    var tiempos_str = session_results.tiempos;
    valor = session_results.resultado;
    numero = toInt_value(no);
    tiempos = toInt_value(tiempos_str);
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

function formatData(array_x,array_y){
    var data = [];
    for (let i = 0; i < array_x.length; i++) {
        data.push({ x:array_x[i], y:array_y[i]});
    }
    return data;
}
