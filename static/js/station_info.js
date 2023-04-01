const API_V1_PREFIX = '/api/v1';
const MONTH = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];

const COLOR_BACKGROUND_RED = 'rgba(255, 99, 132, 0.2)';
const COLOR_BORDER_RED = 'rgba(255, 99, 132, 1)';

const COLOR_BACKGROUND_BLUE = 'rgba(54, 162, 235, 0.2)';
const COLOR_BORDER_BLUE = 'rgba(54, 162, 235, 1)';

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
            backgroundColor: COLOR_BACKGROUND_RED,
            borderColor: COLOR_BORDER_RED,
            borderWidth: 1,
            data: getDatasetByURL('albedo'),
        }
    ]
};

new Chart(
    document.getElementById('albedo'),
    createConfig(dataSet)
)

// ---------------------- ДИФФУЗНАЯ СЛОНЕЧНАЯ РАДИАЦИЯ ----------------------

dataSet = createSolarRadiationDataset('diffuse-monthly','diffuse-daily');

new Chart(
    document.getElementById('diffuse'),
    createConfig(dataSet)
);


// ---------------------- СУММАРНАЯ СЛОНЕЧНАЯ РАДИАЦИЯ ----------------------

dataSet = createSolarRadiationDataset('total-monthly','total-daily');

new Chart(
    document.getElementById('total'),
    createConfig(dataSet)
);

// ---------------------- ПРЯМАЯ СЛОНЕЧНАЯ РАДИАЦИЯ ----------------------

dataSet = createSolarRadiationDataset('direct-monthly','direct-daily');

new Chart(
    document.getElementById('direct'),
    createConfig(dataSet)
);

// ---------------------- ФУНКЦИИ ----------------------

function getDatasetByURL(path) {
    url = window.location.origin + API_V1_PREFIX + window.location.pathname + path;

    request.open('GET', url, false);  // третий аргумент - false для синхронного запроса
    request.send();

    if (request.status === 200) {
        const data = JSON.parse(request.responseText);
        const months = Object.keys(data[0]).filter(key => key.startsWith("month"));
        return months.map(key => +data[0][key]);
    }
}

function createConfig(dataSet) {
    return {
        type: 'line',
        data: dataSet,
        options: {
            maintainAspectRatio: false,
            responsive: true,
            aspectRatio: 1.5, // ширина = высота * 1.5
        }
    };
}

function createSolarRadiationDataset(path1, path2) {
    return {
    labels: MONTH,
    datasets: [
        {
            label: 'Месячная',
            backgroundColor: COLOR_BACKGROUND_RED,
            borderColor: COLOR_BORDER_RED,
            borderWidth: 1,
            data: getDatasetByURL(path1),
        },
        {
            label: 'Суточная',
            backgroundColor: COLOR_BACKGROUND_BLUE,
            borderColor: COLOR_BORDER_BLUE,
            borderWidth: 1,
            data: getDatasetByURL(path2),
        }
    ]
};
}