console.log(hours, minutes, seconds);

(function(){

const hour = document.getElementById('hour');
const mins = document.getElementById('mins');
const secs = document.getElementById('secs');

let S = seconds, M = minutes, H = hours;

console.log(H, M, S);

setInterval(function(){
  //Плюсик перед строкой преобразует его в число
  S = +S +1;
  //Если результат меньше 10, прибавляем впереди строку '0'
  if( S < 10 ) { S = '0' + S;}
  if( S == 60 ) {
    location.reload();
    S = '00';
    //Как только секунд стало 60, добавляем +1 к минутам
    M = +M + 1;
    //Дальше то же самое, что и для секунд
    if( M < 10 ) { M = '0' + M; }
    if( M == 60 ) {
      location.reload();
      //Как только минут стало 60, добавляем +1 к часам.
      M = '00';
      H = +H + 1;
      if( H < 10 ) { H = '0' + H; }
    }
  }
  secs.innerText = S;
  mins.innerText = M;
//  hour.innerText = H;
  //Тикает всё через одну функцию, раз в секунду.
},1000);

})();
