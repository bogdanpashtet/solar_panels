const API_V1_PREFIX = '/api/v1';

const CALCULATE_TYPE_BY_DAY = 'by-day';
const CALCULATE_TYPE_BY_MONTH = 'by-month';
const CALCULATE_TYPE_BY_YEAR = 'by-year';
const CALCULATE_TYPE_BY_CUSTOM = 'by-custom';

const DAY = "day";
const MONTH = "month";
const YEAR = "year";
const CUSTOM = "custom";

const STYLE_BLOCK = "block";
const STYLE_NONE = "none";


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
        switchButtonDo('calculation-type',
            () => {blockStyle(STYLE_BLOCK, STYLE_NONE, STYLE_NONE, STYLE_NONE)},
            () => {blockStyle(STYLE_NONE, STYLE_BLOCK, STYLE_NONE, STYLE_NONE)},
            () => {blockStyle(STYLE_NONE, STYLE_NONE, STYLE_BLOCK, STYLE_NONE)},
            () => {blockStyle(STYLE_NONE, STYLE_NONE, STYLE_NONE, STYLE_BLOCK)}
        );
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
            errorMessage.style.display = STYLE_NONE;
        }

        switchButtonDo('calculation-type',
            () => {createRequest(CALCULATE_TYPE_BY_DAY, 'by-day-day', 'by-day-month')},
            () => {createRequest(CALCULATE_TYPE_BY_MONTH, 'calculation-type-month', 'by-month-month')},
            () => {createRequest(CALCULATE_TYPE_BY_YEAR, 'calculation-type-year')},
            () => {createRequest(CALCULATE_TYPE_BY_CUSTOM, 'num-month-start', 'num-month-end', 'num-day-m-start', 'num-day-m-end')}
        );
    });

function wrapError(message) {
    errorMessage.innerText = message;
    errorMessage.style.display = STYLE_BLOCK;
}

function getRadioButtonValue(radioButtonName) {
    const radioButtons = document.getElementsByName(radioButtonName);
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
            wrapError('Некорректный формат csv.');
        });
}

function blockStyle(style1, style2, style3, style4) {
    document.getElementById(CALCULATE_TYPE_BY_DAY).style.display = style1;
    document.getElementById(CALCULATE_TYPE_BY_MONTH).style.display = style2;
    document.getElementById(CALCULATE_TYPE_BY_YEAR).style.display = style3;
    document.getElementById(CALCULATE_TYPE_BY_CUSTOM).style.display = style4;
}

function createRequest(calcType) {
    let formData = new FormData();
    for (let i = 1; i < arguments.length; i++) {
        let value = arguments[i];
        if (value === "calculation-type-month" || value === "calculation-type-year") {
            formData.append(value, getRadioButtonValue(value));
        } else {
            formData.append(value, document.getElementById(value).value);
        }
    }
    sendRequest(formData, calcType);
}

function switchButtonDo(radioButtonName, ...funcs) {
    switch (getRadioButtonValue(radioButtonName)) {
        case DAY:
            funcs[0]()
            break;
        case MONTH:
            funcs[1]()
            break;
        case YEAR:
            funcs[2]()
            break;
        case CUSTOM:
            funcs[3]()
            break;
    }
}