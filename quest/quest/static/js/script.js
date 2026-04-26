// script.js - таймер для лампового дисплея (оригинальная логика)
(function(){
    const minsTens = document.getElementById('nixie-minutes-tens');
    const minsUnits = document.getElementById('nixie-minutes-units');
    const secsTens = document.getElementById('nixie-seconds-tens');
    const secsUnits = document.getElementById('nixie-seconds-units');

    if (!minsTens || !minsUnits || !secsTens || !secsUnits) return;

    let minutes = parseInt(minsTens.textContent + minsUnits.textContent, 10);
    let seconds = parseInt(secsTens.textContent + secsUnits.textContent, 10);

    if (isNaN(minutes)) minutes = 0;
    if (isNaN(seconds)) seconds = 0;

    function updateDisplay() {
        minsTens.textContent = Math.floor(minutes / 10);
        minsUnits.textContent = minutes % 10;
        secsTens.textContent = Math.floor(seconds / 10);
        secsUnits.textContent = seconds % 10;
    }

    updateDisplay();

    setInterval(function(){
        seconds = seconds + 1;

        if (seconds === 60) {
            location.reload();
            return;
        }

        updateDisplay();
    }, 1000);
})();