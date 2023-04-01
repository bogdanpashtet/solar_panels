const API_V1_PREFIX = '/api/v1'
const MONTH = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

const request = new XMLHttpRequest();

// ---------------------- ИНФОРМАЦИЯ О СТАНЦИИ ----------------------
let url = window.location.origin + API_V1_PREFIX + window.location.pathname;

fetch(url)
    .then(response => response.json())
    .then(data => {
            d3.select('.station_name')
                .text(data[0].station_name);
            d3.select('.station_region')
                .text(data[0].region);
            d3.select('.station_latitude')
                .text(data[0].latitude);
            d3.select('.station_longitude')
                .text(data[0].longitude);
        }
    );

// ---------------------- АЛЬБЕДО ----------------------

let dataSet = {
    labels: MONTH,
    datasets: [
        {
            label: 'Альбедо',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            data: createDataset('albedo'),
        }
    ]
};

let config = {
    type: 'line',
    data: dataSet,
    options: {
        maintainAspectRatio: false,
        responsive: true,
        aspectRatio: 1.5, // ширина = высота * 1.5
    }
};

new Chart(
    document.getElementById('albedo'),
    config
)

// ---------------------- ДИФФУЗНАЯ СЛОНЕЧНАЯ РАДИАЦИЯ ----------------------

dataSet = {
    labels: MONTH,
    datasets: [
        {
            label: 'Месячная',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            data: createDataset('diffuse-monthly'),
        },
        {
            label: 'Суточная',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            data: createDataset('diffuse-daily'),
        }
    ]
};

config = {
    type: 'line',
    data: dataSet,
    options: {
        maintainAspectRatio: false,
        responsive: true,
        aspectRatio: 1.5, // ширина = высота * 1.5
    }
};

new Chart(
    document.getElementById('diffuse'),
    config
)


// ---------------------- СУММАРНАЯ СЛОНЕЧНАЯ РАДИАЦИЯ ----------------------

dataSet = {
    labels: MONTH,
    datasets: [
        {
            label: 'Месячная',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            data: createDataset('total-monthly'),
        },
        {
            label: 'Суточная',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            data: createDataset('total-daily'),
        }
    ]
};

config = {
    type: 'line',
    data: dataSet,
    options: {
        maintainAspectRatio: false,
        responsive: true,
        aspectRatio: 1.5, // ширина = высота * 1.5
    }
};

new Chart(
    document.getElementById('total'),
    config
)

// ---------------------- ПРЯМАЯ СЛОНЕЧНАЯ РАДИАЦИЯ ----------------------

dataSet = {
    labels: MONTH,
    datasets: [
        {
            label: 'Месячная',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            data: createDataset('direct-monthly'),
        },
        {
            label: 'Суточная',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            data: createDataset('direct-daily'),
        }
    ]
};

config = {
    type: 'line',
    data: dataSet,
    options: {
        maintainAspectRatio: false,
        responsive: true,
        aspectRatio: 1.5, // ширина = высота * 1.5
    }
};

new Chart(
    document.getElementById('direct'),
    config
)

function createDataset(path) {
    url = window.location.origin + API_V1_PREFIX + window.location.pathname + path;

    request.open('GET', url, false);  // третий аргумент - false для синхронного запроса
    request.send();

    if (request.status === 200) {
        const data = JSON.parse(request.responseText);
        const months = Object.keys(data[0]).filter(key => key.startsWith("month"));
        return months.map(key => +data[0][key]);
    }
}