const API_V1_PREFIX = '/api/v1';

let file = null;
document.getElementById('load-csv-button')
    .addEventListener('change', function () {
        file = this.files[0];
    });

document.querySelector('#calculate-button')
    .addEventListener('click', () => {
        if (!file) {
            console.error('Файл не выбран');
            return;
        }

        let url = window.location.origin + API_V1_PREFIX + window.location.pathname + 'by-day';
        const formData = new FormData();
        formData.append('file', file);


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
                console.error('Ошибка:', error);
            });
    });