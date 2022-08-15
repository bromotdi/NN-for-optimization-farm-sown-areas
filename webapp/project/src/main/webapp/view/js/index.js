var backendResponse = ['соняшник', 'овес', 'овес', 'овес', 'горох', 'пшениця', 'пар', 'люпин на зерно', 'пар', 'соняшник', 64600];
var fieldsContainer = document.getElementById('fieldsContainer');
var cropsPercentage = document.getElementById('cropsPercentage');
var income = document.getElementById('income');

var colors = {
    'кукуруза': '#F7E78F',
    'жито': '#B6AD9E',
    'картопля рання': '#BCA796',
    'овес': '#F0E7D6',
    'ячмінь': '#E9DDC7',
    'пшениця': '#F6D294',
    'горох': '#EEFFAF',
    'люпин на зерно': '#90C1BB',
    'цукрові буряки': '#D5DEC9',
    'льон': '#F5DDFD',
    'соняшник': '#FFC72C',
    'пар': '#CEE2C7'
}

// генерация div-элемента для одного поля
function createField(text) {
    var div = document.createElement('div');
    div.textContent = text;
    return div;
}

// генерация полей для визуализации
function getFields() {
    document.querySelectorAll('.field').forEach(e => e.remove()); // очистка fieldsContainer от предыдущих значений

    let num = 1;
    backendResponse.slice(0, backendResponse.length - 1)
        .forEach(child => {
            color = colors[child];
            child = createField(num);
            child.className = 'field';
            child.style.backgroundColor = color;
            fieldsContainer.appendChild(child);
            num++;
        });
}


function createPercentage(crop, percentage) {
    var div = document.createElement('div');

    var bullet = document.createElement('p');
    var text = document.createElement('p');

    bullet.textContent = '•';
    bullet.className = 'bullelements';
    bullet.style.color = colors[crop];
    text.textContent = percentage + '% ' + crop;

    div.appendChild(bullet);
    div.appendChild(text);

    return div;
}

function getPercentages() {
    // подсчет кол-ва полей для каждой культуры
    var uniqs = backendResponse.slice(0, backendResponse.length - 1)
        .reduce((acc, val) => {
            acc[val] = acc[val] === undefined ? 1 : acc[val] += 1;
            return acc;
        }, {});


    document.querySelectorAll('.percentage').forEach(e => e.remove()); // очистка cropsPercentage от предыдущих значений

    // сортування за спаданням
    function compareSecondColumn(a, b) {
        if (a[1] === b[1]) {
            return 0;
        }
        else {
            return (a[1] > b[1]) ? -1 : 1;
        }
    }

    for (const [key, value] of Object.entries(uniqs).sort(compareSecondColumn)) {
        child = createPercentage(key, value * 100 / (backendResponse.length - 1));
        child.className = 'percentage';
        cropsPercentage.appendChild(child);
    }
}

// доход
function getIncome() {
    document.querySelectorAll('.incomeText').forEach(e => e.remove()); // очистка от предыдущих значений
    var text = document.createElement('p');
    text.className = 'incomeText';
    text.textContent = 'Очікуваний дохід: ' + backendResponse[backendResponse.length - 1];
    income.appendChild(text);
}

function getResult() {
    getFields();
    getPercentages();
    getIncome();
}