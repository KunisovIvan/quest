// script.js - таймер для уровня
(function(){
    const minsDiv = document.getElementById('mins');
    const secsDiv = document.getElementById('secs');

    // Если элементов нет – выходим
    if (!minsDiv || !secsDiv) return;

    // Берём начальные значения из текста элементов (уже пришли из шаблона)
    let M = parseInt(minsDiv.innerText, 10);
    let S = parseInt(secsDiv.innerText, 10);

    // Функция форматирования с ведущим нулём
    function format(num) {
        return num < 10 ? '0' + num : '' + num;
    }

    // Показываем форматированные значения сразу
    minsDiv.innerText = format(M);
    secsDiv.innerText = format(S);

    setInterval(function(){
        S = S + 1;

        if (S === 60) {
            location.reload();  // перезагрузка страницы раз в минуту
            return;
        }

        secsDiv.innerText = format(S);
        minsDiv.innerText = format(M);
    }, 1000);
})();