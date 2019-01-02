var socket = io('http://127.0.0.1:5000');

var description_decode;
var numero = 1;

function startTraining() {
  numero = 1;
  document.getElementById("button_start").style.display = "none";
  var description = document.getElementById("generate_description").textContent;
  description_decode = JSON.parse(description);
  var session = document.getElementById("session_description").textContent;
  session_decode = JSON.parse(session);
  id = session_decode.id;
  document.getElementById('session_id').value = id;
  tiempo = description_decode.time;
  secuencial = description_decode.is_secuencial;
  reps = description_decode.reps;
  modules = description_decode.modules;
  tipo = description_decode.typeReaction;
  console.log(tiempo, secuencial, reps, modules, tipo);
  temporizador(tiempo);
  socket.emit("entrenamiento general", tipo,tiempo,reps,modules,secuencial);
}

function startGame() {
  numero = 1;
  document.getElementById("button_start").style.display = "none";
  var description = document.getElementById("generate_description").textContent;
  description_decode = JSON.parse(description);
  var session = document.getElementById("session_description").textContent;
  session_decode = JSON.parse(session);
  id = session_decode.id;
  document.getElementById('session_id').value = id;
  tiempo = description_decode.time;
  secuencial = description_decode.is_secuencial;
  reps = description_decode.reps;
  modules = description_decode.modules;
  tipo = description_decode.typeReaction;
  juego = description_decode.name;
  if (juego === 'Juego 1'){
    var no_random = randomInt(10,20);
    socket.emit(juego,no_random);
  }
  else{
    socket.emit(juego);
  }
}

function startCapture(){
  numero = 1;
  var session = document.getElementById("session_description").textContent;
  session_decode = JSON.parse(session);
  id = session_decode.id;
  time_activation = session_decode.time_activation;
  document.getElementById('session_id').value = id;
  document.getElementById("button_start").style.display = "none";
  document.getElementById("button_stop").style.display = "block";
  socket.emit('modo captura',time_activation);
  cronometro();
}

function finishCapture (){
  document.getElementById("button_stop").style.display = "none";
  socket.emit('fin captura');
  stopCronometro();
}

//Recepcion de canales de Socket.io y sus acciones correspondientes 

  socket.on('results', function(tiempo,mensaje){
    introduceResults(tiempo,mensaje);
    numero = numero + 1;
  });

  socket.on('entrenamiento finalizado', function(){
    getCellValues();
    document.getElementById("save_results").style.display = "block";
  })

//Insertar resultados
function introduceResults(tiempo,message) {
  var table = document.getElementById("results_table");
  var row = table.insertRow(-1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  cell1.innerHTML = numero;
  cell2.innerHTML = tiempo;
  cell3.innerHTML = message;
}

function getCellValues() {
  var no = [];
  var times = [];
  var result = [];
  var table = document.getElementById('results_table');
  for (var r = 0, n = table.rows.length; r < n; r++) {
      for (var c = 0, m = table.rows[r].cells.length; c < m; c++) {
        if(c === 0){
           no.push(table.rows[r].cells[c].innerHTML);   
        }
        if(c === 1){
            times.push(table.rows[r].cells[c].innerHTML); 
        }
        if (c === 2){
            result.push(table.rows[r].cells[c].innerHTML); 
        }

      }
  }
  var time_number = [];
  var suma = 0;
  for (var i = 0; i < times.length; i++) {
      if (isNaN(times[i]) === true){
      }
      else{
        time_number.push(parseInt(times[i])); 
      }   
  }
  for ( var i = 0; i < time_number.length; i++) {
    suma = suma + time_number[i];
  }
  var num = time_number.length;
  var promedio = suma/num;
  promedio = promedio.toFixed(2); 
  var minimo = Math.min(...time_number);
  var maximo = Math.max(...time_number);
  var resultados_destacados = [minimo,maximo, promedio]

  var results = {numero:no, tiempos:times, resultado:result, resumen:resultados_destacados};
  var myJSON = JSON.stringify(results);
  document.getElementById('generate_results').value = myJSON;
}


function postResults() {
  document.getElementById("results").submit();
}

//Obtener el color seleccionado para los módulos
function colorSelect() {
  if (document.getElementById("rdbtn1").checked) {
    moduloColor = "blue";
  }
  if (document.getElementById("rdbtn2").checked) {
    moduloColor = "red";
  }
  if (document.getElementById("rdbtn3").checked) {
    moduloColor = "green";
  }
  console.log(moduloColor);
}


function temporizador(time){
  var tiempo = time;
  var x = setInterval(function(){

    minutes = (tiempo / 60) | 0;
    seconds = (tiempo % 60) | 0;
    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;
    document.getElementById("timer").innerHTML = minutes +" : " + seconds;
    tiempo--;

    if(seconds == 00 && minutes > 0){
      minutes--;
      seconds = 60;
      if (minutes == 0){
         minutes = 0;
      }
    }
    if (seconds <= 00 && minutes <= 0) {
      clearInterval(x);
      document.getElementById("timer").innerHTML = "Entrenamiento finalizado";
    }

  },1000);
}

function cronometro(){
    minutes = 0;
    seconds = 0;
 x = setInterval(function(){
    seconds = seconds < 10 ? "0" + seconds : seconds;
    document.getElementById("timer").innerHTML = minutes +" : " + seconds;
    seconds++;
    if (seconds >= 60){
         minutes++;
         seconds = 0;
    }
  },1000);
}

function stopCronometro(){
  clearInterval(x);
  document.getElementById("timer").innerHTML = "Entrenamiento finalizado";
}

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}