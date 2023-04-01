const API_V1_PREFIX = '/api/v1'
const MONTH = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

// получаем информацию о станции
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

// получаем альбедо
url = window.location.origin + API_V1_PREFIX + window.location.pathname + 'albedo';

let albedo_values

fetch(url)
    .then(response => response.json())
    .then(data => {
            const months = Object.keys(data[0]).filter(key => key.startsWith("month"));
            albedo_values = months.map(key => +data[0][key]);

            const dataSet = {
                labels: MONTH,
                datasets: [
                    {
                        label: 'Альбедо',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                        data: albedo_values,
                    }
                ]
            };

            const config = {
                type: 'line',
                data: dataSet,
                options: {
                    maintainAspectRatio: false,
                    responsive: true,
                    aspectRatio: 1.5, // ширина = высота * 1.5
                }
            };

            const albedo = new Chart(
                document.getElementById('albedo'),
                config
            )
        }
    );

// ---------------------- ДИФФУЗНАЯ СЛОНЕЧНАЯ РАДИАЦИЯ ----------------------

// Месячная
url = window.location.origin + API_V1_PREFIX + window.location.pathname + 'diffuse-monthly';

const request = new XMLHttpRequest();
request.open('GET', url, false);  // третий аргумент - false для синхронного запроса
request.send();

let diffuse_month = [];

if (request.status === 200) {
    const data = JSON.parse(request.responseText);
    const months = Object.keys(data[0]).filter(key => key.startsWith("month"));
    diffuse_month = months.map(key => +data[0][key]);
}

// Суточная
url = window.location.origin + API_V1_PREFIX + window.location.pathname + 'diffuse-daily';
request.open('GET', url, false);  // третий аргумент - false для синхронного запроса
request.send();

let diffuse_daily = [];

if (request.status === 200) {
    const data = JSON.parse(request.responseText);
    const months = Object.keys(data[0]).filter(key => key.startsWith("month"));
    diffuse_daily = months.map(key => +data[0][key]);
}

let dataSet = {
    labels: MONTH,
    datasets: [
        {
            label: 'Месячная',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            data: diffuse_month,
        },
        {
            label: 'Суточная',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            data: diffuse_daily,
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

let diffuse = new Chart(
    document.getElementById('diffuse'),
    config
)


// ---------------------- СУММАРНАЯ СЛОНЕЧНАЯ РАДИАЦИЯ ----------------------

// Месячная
url = window.location.origin + API_V1_PREFIX + window.location.pathname + 'total-monthly';

request.open('GET', url, false);  // третий аргумент - false для синхронного запроса
request.send();

let total_month = [];

if (request.status === 200) {
    const data = JSON.parse(request.responseText);
    const months = Object.keys(data[0]).filter(key => key.startsWith("month"));
    total_month = months.map(key => +data[0][key]);
}

// Суточная
url = window.location.origin + API_V1_PREFIX + window.location.pathname + 'total-daily';
request.open('GET', url, false);  // третий аргумент - false для синхронного запроса
request.send();

let total_daily = [];

if (request.status === 200) {
    const data = JSON.parse(request.responseText);
    const months = Object.keys(data[0]).filter(key => key.startsWith("month"));
    total_daily = months.map(key => +data[0][key]);
}

dataSet = {
    labels: MONTH,
    datasets: [
        {
            label: 'Месячная',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            data: total_month,
        },
        {
            label: 'Суточная',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            data: total_daily,
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

const total = new Chart(
    document.getElementById('total'),
    config
)


// ---------------------- ПРЯМАЯ СЛОНЕЧНАЯ РАДИАЦИЯ ----------------------

// Месячная
url = window.location.origin + API_V1_PREFIX + window.location.pathname + 'direct-monthly';

request.open('GET', url, false);  // третий аргумент - false для синхронного запроса
request.send();

let direct_month = [];

if (request.status === 200) {
    const data = JSON.parse(request.responseText);
    const months = Object.keys(data[0]).filter(key => key.startsWith("month"));
    direct_month = months.map(key => +data[0][key]);
}

// Суточная
url = window.location.origin + API_V1_PREFIX + window.location.pathname + 'direct-daily';
request.open('GET', url, false);  // третий аргумент - false для синхронного запроса
request.send();

let direct_daily = [];

if (request.status === 200) {
    const data = JSON.parse(request.responseText);
    const months = Object.keys(data[0]).filter(key => key.startsWith("month"));
    direct_daily = months.map(key => +data[0][key]);
}

dataSet = {
    labels: MONTH,
    datasets: [
        {
            label: 'Месячная',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            data: direct_month,
        },
        {
            label: 'Суточная',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            data: direct_daily,
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

const direct = new Chart(
    document.getElementById('direct'),
    config
)