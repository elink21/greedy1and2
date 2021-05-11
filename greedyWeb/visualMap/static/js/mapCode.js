var map = new L.map("map").setView([19.407, -99.17], 6);


function resetMap() {
    map.remove();

    map = new L.map("map").setView([19.407, -99.17], 6);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);
    addCities(map, cities);

}

function sendData() {
    const sel = document.querySelector('#select').value;
    $.ajax({
        url: 'greedyA',
        data: { 'initialNode': sel },
        success: function (data) {
            updateTable(data['route'], data['distance']);
            resetMap();
            drawLines(data['route'], map);
        }
    });
}

function greedyB() {
    $.ajax({
        url: 'greedyB',
        data: {},
        success: function (data) {
            updateTable(data['route'], data['distance']);
            resetMap();
            drawLines(data['route'], map)
        }
    });
}

function drawLines(route, map) {
    for (let r of route) {
        let from = names[r['from']];
        let to = names[r['to']];
        L.polyline([cities[from], cities[to]]).addTo(map);
    }
}

function updateTable(newRoute, totalDistance) {
    let tBody = document.querySelector("#tBody");
    tBody.innerHTML = '';

    for (let r of newRoute) {
        let newRow = `<tr>
        <td>${names[r['from']]}</td>
        <td>${names[r['to']]}</td>
        <td>${r['distance']}</td>
      </tr > `
        tBody.innerHTML += newRow;
    }

    let newRow = `<tr>
        <td><strong>Total</strong></td>
        <td> = </td>
        <td>${totalDistance}</td>
      </tr > `;

    tBody.innerHTML += newRow;

}


function addCities(map, cities) {
    for (const city of Object.keys(cities)) {
        L.marker(cities[city]).addTo(map).bindTooltip(city);
    }
}




L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

addCities(map, cities);
