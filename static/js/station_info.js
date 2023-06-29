const API_V1_PREFIX = '/insolation_for_horizontal_panels/v1';
const MONTH = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
const HOURS = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', '23-24'];

const MONTH_INDEX = 15; // если нужна информация по месяцам обозначим за 15

const COLOR_BACKGROUND_RED = 'rgba(255, 99, 132, 0.2)';
const COLOR_BORDER_RED = 'rgba(255, 99, 132, 1)';

const COLOR_BACKGROUND_BLUE = 'rgba(54, 162, 235, 0.2)';
const COLOR_BORDER_BLUE = 'rgba(54, 162, 235, 1)';

const COLOR_BACKGROUND_YELLOW = 'rgba(255, 206, 86, 0.2)';
const COLOR_BORDER_YELLOW = 'rgba(255, 206, 86, 1)';

const request = new XMLHttpRequest();

// ---------------------- ИНФОРМАЦИЯ О СТАНЦИИ ----------------------
let url = window.location.origin + API_V1_PREFIX + window.location.pathname;

fetch(url)
    .then(response => response.json())
    .then(data => {
            document.getElementById("station_name").textContent = data[0].station_name;
            document.getElementById("station_region").textContent = data[0].region;
            document.getElementById("station_latitude").textContent = data[0].latitude;
            document.getElementById("station_longitude").textContent = data[0].longitude;
        }
    );

// ---------------------- ЗАПОЛНЯЕМ ТАБЛИЦЫ ----------------------
createTable('diffuse-hourly');
createTable('total-hourly');
createTable('direct-hourly');

// ---------------------- ССЫЛКИ НА СКАЧИВАНИЕ ----------------------
createDownloadLink('#download-csv-btn-diffuse', 'diffuse-hourly/csv');
createDownloadLink('#download-csv-btn-total', 'total-hourly/csv');
createDownloadLink('#download-csv-btn-direct', 'direct-hourly/csv');


// ---------------------- АЛЬБЕДО ----------------------

let dataSet = {
    labels: MONTH,
    datasets: [
        {
            label: 'Альбедо',
            backgroundColor: COLOR_BACKGROUND_RED,
            borderColor: COLOR_BORDER_RED,
            borderWidth: 1,
            data: getDatasetMonthByURL('albedo', MONTH_INDEX),
        }
    ]
};

new Chart(
    document.getElementById('albedo'),
    createConfig(dataSet)
)

// ---------------------- МЕСЯЧНЫЕ СУММЫ СОЛНЕЧНОЙ РАДИАЦИИ ----------------------
dataSet = createSolarRadiationDataset(MONTH, MONTH_INDEX, 'diffuse-monthly', 'direct-monthly', 'total-monthly');

new Chart(
    document.getElementById('monthly'),
    createConfig(dataSet)
);

// ---------------------- СРЕДЕМЕСЯЧНЫЙ ПРИХОД ДЛЯ ИЮНЯ ----------------------
dataSet = createSolarRadiationDataset(HOURS, 5, 'diffuse-hourly', 'direct-hourly', 'total-hourly');

new Chart(
    document.getElementById('june'),
    createConfig(dataSet)
);

// ---------------------- СРЕДЕМЕСЯЧНЫЙ ПРИХОД ДЛЯ ЯНВАРЯ ----------------------
dataSet = createSolarRadiationDataset(HOURS, 0, 'diffuse-hourly', 'direct-hourly', 'total-hourly');

new Chart(
    document.getElementById('january'),
    createConfig(dataSet)
);

// ---------------------- ФУНКЦИИ ----------------------

function getDatasetMonthByURL(path, index) {
    url = window.location.origin + API_V1_PREFIX + window.location.pathname + path;

    request.open('GET', url, false);  // третий аргумент - false для синхронного запроса
    request.send();

    if (request.status === 200) {
        const data = JSON.parse(request.responseText);
        if (index === MONTH_INDEX) {
            const months = Object.keys(data[0]).filter(key => key.startsWith("month"));
            return months.map(key => +data[0][key]);
        } else {
            let arr = [];
            for (let i = 0; i < 24; i++) {
                arr.push(getDataMonth(i, index, data));
            }
            return arr
        }
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

function createSolarRadiationDataset(label, index, path1, path2, path3) {
    return {
        labels: label,
        datasets: [
            {
                label: 'Диффузная',
                backgroundColor: COLOR_BACKGROUND_RED,
                borderColor: COLOR_BORDER_RED,
                borderWidth: 1,
                data: getDatasetMonthByURL(path1, index),
            },
            {
                label: 'Прямая',
                backgroundColor: COLOR_BACKGROUND_BLUE,
                borderColor: COLOR_BORDER_BLUE,
                borderWidth: 1,
                data: getDatasetMonthByURL(path2, index),
            },
            {
                label: 'Суммарная',
                backgroundColor: COLOR_BACKGROUND_YELLOW,
                borderColor: COLOR_BORDER_YELLOW,
                borderWidth: 1,
                data: getDatasetMonthByURL(path3, index),
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

function createDownloadLink(button_id, path) {
    document.querySelector(button_id)
        .addEventListener('click', () => {
            url = window.location.origin + API_V1_PREFIX + window.location.pathname + path;

            const link = document.createElement('a');
            link.href = url;
            link.click();
        });
}