// script.js - все скрипты для сайта

// 1. Случайное фото
(function(){
    const randomPhotoContainer = document.getElementById('random-photo');
    if (randomPhotoContainer) {
        const images = [
            '1.png', '2.png', '3.png', '4.png', '5.png',
            '6.png', '7.png', '8.png', '9.png', '10.png',
            '11.png', '12.jpg'
        ];
        const randomImage = images[Math.floor(Math.random() * images.length)];
        // Получаем базовый путь из data-атрибута или из статики
        const staticPath = randomPhotoContainer.getAttribute('data-static-path') || '/static/images/';
        randomPhotoContainer.src = staticPath + randomImage;
    }
})();

// 2. Таймер для уровня
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