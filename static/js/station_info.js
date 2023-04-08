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

createTable('diffuse-hourly');
createTable('total-hourly');
createTable('direct-hourly');


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

dataSet = createSolarRadiationDataset('diffuse-monthly', 'diffuse-daily');

new Chart(
    document.getElementById('diffuse'),
    createConfig(dataSet)
);

// ---------------------- СУММАРНАЯ СЛОНЕЧНАЯ РАДИАЦИЯ ----------------------

dataSet = createSolarRadiationDataset('total-monthly', 'total-daily');

new Chart(
    document.getElementById('total'),
    createConfig(dataSet)
);

// ---------------------- ПРЯМАЯ СЛОНЕЧНАЯ РАДИАЦИЯ ----------------------

dataSet = createSolarRadiationDataset('direct-monthly', 'direct-daily');

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

function createTable(tableName) {
    url = window.location.origin + API_V1_PREFIX + window.location.pathname + tableName;

    fetch(url)
        .then(response => response.json())
        .then(data => {
                const table = document.getElementById(tableName);
                const tbody = table.querySelector("tbody");

                for (let j = 0; j < 12; j++) {
                    let row = document.createElement('tr');
                    addCell(MONTH[j], row);
                    for (let i = 0; i < 24; i++) {
                        let dataMonth = getDataMonth(i, j, data);
                        addCell(dataMonth, row);
                    }
                    tbody.appendChild(row);
                }
            }
        );
}

function addCell(cellData, row) {
    let cell = document.createElement('td');
    cell.textContent = cellData;
    row.appendChild(cell);
}

function getDataMonth(i, j, data) {
    switch (j) {
        case 0:
            return data[i].month_1;
        case 1:
            return data[i].month_2;
        case 2:
            return data[i].month_3;
        case 3:
            return data[i].month_4;
        case 4:
            return data[i].month_5;
        case 5:
            return data[i].month_6;
        case 6:
            return data[i].month_7;
        case 7:
            return data[i].month_8;
        case 8:
            return data[i].month_9;
        case 9:
            return data[i].month_10;
        case 10:
            return data[i].month_11;
        case 11:
            return data[i].month_12;
    }
}