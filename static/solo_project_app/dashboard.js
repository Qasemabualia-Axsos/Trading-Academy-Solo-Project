function randomFluctuation(rate) {
    if (!rate) return '--';
    let change = (Math.random() * 0.0005) - 0.00025;
    return (parseFloat(rate) + change).toFixed(4);
}

function updateRates() {
    fetch('/api/get_forex_rates/')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('USD_to_EUR').innerText = '--';
                document.getElementById('EUR_to_USD').innerText = '--';
                document.getElementById('last_updated').innerText = 'Error fetching rates';
                console.error('API error:', data.error);
            } else {
                document.getElementById('USD_to_EUR').innerText = randomFluctuation(data.USD_to_EUR);
                document.getElementById('EUR_to_USD').innerText = randomFluctuation(data.EUR_to_USD);
                document.getElementById('USD_to_GBP').innerText = randomFluctuation(data.USD_to_GBP);
                document.getElementById('GBP_to_USD').innerText = randomFluctuation(data.GBP_to_USD);
                document.getElementById('USD_to_JPY').innerText = randomFluctuation(data.USD_to_JPY);
                document.getElementById('JPY_to_USD').innerText = randomFluctuation(data.JPY_to_USD);
                document.getElementById('USD_to_AUD').innerText = randomFluctuation(data.USD_to_AUD);
                document.getElementById('AUD_to_USD').innerText = randomFluctuation(data.AUD_to_USD);
                document.getElementById('USD_to_CAD').innerText = randomFluctuation(data.USD_to_CAD);
                document.getElementById('CAD_to_USD').innerText = randomFluctuation(data.CAD_to_USD);

                document.getElementById('last_updated').innerText = new Date().toLocaleTimeString();
            }
        })
        .catch(err => {
            document.getElementById('USD_to_EUR').innerText = '--';
            document.getElementById('EUR_to_USD').innerText = '--';
            document.getElementById('last_updated').innerText = 'Error fetching rates';
            console.error('Fetch error:', err);
        });
}

// Run immediately and every 5 seconds
updateRates();
setInterval(updateRates, 5000);