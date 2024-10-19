const screens = document.querySelectorAll('.screen');
const indicators = document.querySelectorAll('.indicator');

function showScreen(index) {
    screens.forEach(screen => screen.classList.remove('active'));
    indicators.forEach(indicator => indicator.classList.remove('active'));
    screens[index].classList.add('active');
    indicators[index].classList.add('active');
}

function changeTemp(delta) {
    const tempElement = document.getElementById('temp-value');
    let currentTemp = parseInt(tempElement.textContent);
    currentTemp += delta;
    tempElement.textContent = currentTemp;
}

function updateTime() {
    const timeDisplay = document.getElementById('time-display');
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    timeDisplay.textContent = `${hours}:${minutes}:${seconds}`;
}

// Initialize time display
updateTime();
setInterval(updateTime, 1000);

// Add event listeners to indicators
indicators.forEach((indicator, index) => {
    indicator.addEventListener('click', () => showScreen(index));
});
