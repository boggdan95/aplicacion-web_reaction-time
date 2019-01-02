window.onload = function () {

    var resultTimes = document.getElementById('chartContainer');
    getData();
    stringResult(valor);
    console.log(tiempos);
    
    var minimo = Math.min(...tiempo_noZero);
    var maximo = Math.max(...tiempos);
    var promedio = average(tiempo_noZero);
    promedio = promedio.toFixed(2);
    
    document.getElementById("minimo_value").innerHTML = minimo + 'ms.';
    document.getElementById("maximo_value").innerHTML = maximo + 'ms.';
    document.getElementById("average_value").innerHTML = promedio + 'ms.';
    document.getElementById("hit_value").innerHTML = acierto;
    document.getElementById("fail_value").innerHTML = fallo;
    document.getElementById("error_value").innerHTML = error;

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
    generateTable();
    
    }

    

function getData(){
    var session = document.getElementById("session_data").textContent;
    var session_decode = JSON.parse(session);
    id = session_decode.id;
    console.log(session_decode);
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

function formatData(array_x,array_y){
    var data = [];
    for (let i = 0; i < array_x.length; i++) {
        data.push({ x:array_x[i], y:array_y[i]});
    }
    return data;
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

function generateTable() {
    // Obtener la referencia del elemento body
    var body = document.getElementById("content");
    // Crea un elemento <table> y un elemento <tbody>
    var tabla   = document.createElement("table");
    var tblBody = document.createElement("tbody");
    tabla.setAttribute("id", "results_table");
    tabla.setAttribute("class", "text2");

    var tiempos_rst = tiempos;
    var numero_rst = numero;
    tiempos_rst.unshift('Tiempos');
    numero_rst.unshift('Intento');
    // Crea las celdas
    for (var i = 0; i < numero.length; i++) {
        // Crea las hileras de la tabla
        var hilera = document.createElement("tr");

        for (var j = 0; j < 3; j++) {
        // Crea un elemento <td> y un nodo de texto, haz que el nodo de
        // texto sea el contenido de <td>, ubica el elemento <td> al final
        // de la hilera de la tabla
            if (j === 0) {
                var celda = document.createElement("td");
                var textoCelda = document.createTextNode(numero_rst[i]); 
            }
            if (j === 1) {
                var celda = document.createElement("td");
                var textoCelda = document.createTextNode(tiempos_rst[i]);
            }
            if( j === 2){
                var celda = document.createElement("td");
                var textoCelda = document.createTextNode(valor[i]);
            }
        celda.appendChild(textoCelda);
        hilera.appendChild(celda);
        }
        // agrega la hilera al final de la tabla (al final del elemento tblbody)
        tblBody.appendChild(hilera);
    }
    
    // posiciona el <tbody> debajo del elemento <table>
    tabla.appendChild(tblBody);
    // appends <table> into <body>
    body.appendChild(tabla);
    }

    function downloadCSV(csv, filename) {
        var csvFile;
        var downloadLink;    
        // CSV file
        csvFile = new Blob([csv], {type: "text/csv"});
        // Download link
        downloadLink = document.createElement("a");
        // File name
        downloadLink.download = filename;
        // Create a link to the file
        downloadLink.href = window.URL.createObjectURL(csvFile);
        // Hide download link
        downloadLink.style.display = "none";
        // Add the link to DOM
        document.body.appendChild(downloadLink);
        // Click download link
        downloadLink.click();
    }


    function exportTableToCSV() {
        var csv = [];
        var rows = document.querySelectorAll("table tr");
        
        for (var i = 0; i < rows.length; i++) {
            var row = [], cols = rows[i].querySelectorAll("td, th");
            
            for (var j = 0; j < cols.length; j++) 
                row.push(cols[j].innerText);
            
            csv.push(row.join(","));        
        }
        var filename = 'results-session-'+id+'.csv';
        console.log(filename);
        
        // Download CSV file
        downloadCSV(csv.join("\n"),filename);
    }