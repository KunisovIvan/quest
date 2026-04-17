// script.js - таймер для уровня
(function(){
    const minsDiv = document.getElementById('mins');
    const secsDiv = document.getElementById('secs');
    // Переменные seconds, minutes, hours приходят из шаблона (глобальные)
    let S = window.seconds || 0;
    let M = window.minutes || 0;
    let H = window.hours || 0;

    if (!minsDiv || !secsDiv) return; // если нет элементов таймера – выходим

    setInterval(function(){
        S = +S + 1;
        if (S < 10) { S = '0' + S; }
        if (S == 60) {
            S = '00';
            M = +M + 1;
            if (M < 10) { M = '0' + M; }
            if (M == 60) {
                M = '00';
                H = +H + 1;
                if (H < 10) { H = '0' + H; }
            }
        }
        minsDiv.innerText = M;
        secsDiv.innerText = S;
    }, 1000);
})();