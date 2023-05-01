const API_V1_PREFIX = '/api/v1';
const CALCULATE_BY_DAY_ENDPOINT = 'by-day';
const CALCULATE_BY_MONTH_ENDPOINT = 'by-month';
const CALCULATE_BY_YEAR_ENDPOINT = 'by-year';
const CALCULATE_BY_CUSTOM_ENDPOINT = 'by-custom';

const errorMessage = document.getElementById('error-message');

// Добавляем файл
let file = null;
document.getElementById('load-csv-button')
    .addEventListener('change', function () {
        file = this.files[0];
    });

// Событие обрабатываемое, при смене положения radio-button
document.querySelectorAll('input[name="calculation-type"]').forEach(radio => {
    radio.addEventListener('change', () => {
        const value = radio.value;
        switch (getRadioButtonName()) {
            case 'day':
                document.getElementById('by-day-field-container').style.display = 'block';
                document.getElementById('by-day-day').value = '';
                document.getElementById('by-day-month').value = '';
                break;
            case 'month':
                document.getElementById('by-day-field-container').style.display = 'none';
                break;
            case 'year':
                document.getElementById('by-day-field-container').style.display = 'none';
                break;
            case 'custom':
                document.getElementById('by-day-field-container').style.display = 'none';
                break;
        }
    });
});

// Обработка нажатия на кнопку "Рассчитать"
document.querySelector('#calculate-button')
    .addEventListener('click', () => {
        if (!file) {
            wrapError('Файл не выбран.');
            return;
        } else if (file.type !== "text/csv") {
            wrapError('Невенрный формат файла: выберете ".csv".');
            return;
        } else {
            errorMessage.style.display = 'none';
        }

        let formData = new FormData();

        switch (getRadioButtonName()) {
            case 'day':
                formData = new FormData();
                formData.append('by-day-day', document.getElementById('by-day-day').value);
                formData.append('by-day-month', document.getElementById('by-day-month').value);
                sendRequest(formData, CALCULATE_BY_DAY_ENDPOINT);
                break;
            case 'month':
                formData = new FormData();

                sendRequest(formData, CALCULATE_BY_MONTH_ENDPOINT);
                break;
            case 'year':
                formData = new FormData();

                sendRequest(formData, CALCULATE_BY_YEAR_ENDPOINT);
                break;
            case 'custom':
                formData = new FormData();

                sendRequest(formData, CALCULATE_BY_CUSTOM_ENDPOINT);
                break;
        }
    });

function wrapError(message) {
    errorMessage.innerText = message;
    errorMessage.style.display = 'block';
}

function getRadioButtonName() {
    const radioButtons = document.getElementsByName('calculation-type');
    let selectedValue = '';
    for (const button of radioButtons) {
        if (button.checked) {
            selectedValue = button.value;
            break;
        }
    }
    return selectedValue
}

function getMaxAngleState() {
    return !!document.getElementById('calculate-max-angle').checked;
}

function sendRequest(formData, endpoint) {
    let url = window.location.origin + API_V1_PREFIX + window.location.pathname + endpoint;

    formData.append('file', file);
    if (getMaxAngleState() === false) {
        formData.append('max-angle', 'false');
        formData.append('tilt-angle', document.getElementById('tilt-angle').value);
    } else {
        formData.append('max-angle', 'true');
    }
    formData.append('latitude', document.getElementById('latitude').value);
    formData.append('azimuth', document.getElementById('azimuth').value);
    formData.append('by-day-day', document.getElementById('by-day-day').value);
    formData.append('by-day-month', document.getElementById('by-day-month').value);

    fetch(url,
        {
            method: 'POST',
            body: formData
        }
    )
        .then(response => response.json())
        .then(data => {
            console.log(data)
        })
        .catch(error => {
            wrapError('Некорпектный формат csv.');
        });
}