const API_V1_PREFIX = '/api/v1'

const svg = d3.select('svg')
    .style('transition', 'transform 0.3s ease-in-out');

const projection = d3.geoMercator()
    .scale(300)
    .center([0, 0])
    .translate([-50, 800]);

const pathGenerator = d3.geoPath().projection(projection);

const zoom = d3.zoom()
    .scaleExtent([1, 8])
    .on("zoom", zoomed);

const g = svg.append("g");

function zoomed(event) {
    const {transform} = event;
    g.attr("transform", transform);
    g.attr("stroke-width", 1 / transform.k);

    g.selectAll("circle")
        .style('stroke-width', 1 / transform.k)
        .attr('r', 5 / transform.k);
}

d3.json('static/json/ussr.json')
    .then(data => {
        const countries = topojson.feature(data, data.objects.countries)

        g.selectAll('path')
            .data(countries.features)
            .enter().append('path')
            .attr("fill", "#ccc")
            .attr("stroke", "#333")
            .on("dblclick.zoom", null)
            .attr('d', d => pathGenerator(d));

        createPoints();
    });

svg.call(zoom);

function createPoints() {
    let url = window.location.origin + API_V1_PREFIX + '/stations';

    fetch(url)
        .then(response => response.json())
        .then(data => {

                data.forEach(function (d) {
                    d.latitude = +d.latitude;
                    d.longitude = +d.longitude;
                    d.id = d.id.toString();
                });

                g.selectAll("g")
                    .data(data)
                    .enter()
                    .append("g")
                    .append("a")
                    .attr("xlink:href", d => {
                        return window.location.origin + '/station/' + d.id;
                    })
                    .append("circle")
                    .attr("id", d => {
                        return d.id;
                    })
                    .attr("cx", d => {
                        return projection([d.longitude, d.latitude])[0];
                    })
                    .attr("cy", d => {
                        return projection([d.longitude, d.latitude])[1];
                    })
                    .attr("r", 5)
                    .style("fill", "red")
                    .style("stroke", "black")
                    .style("stroke-width", 1)
                    .on("mouseover", function () {
                        let size = d3.select(this).attr('r')

                        d3.select(this)
                            .style("fill", "lightgreen")
                            .attr("r", size * 1.3);
                    })
                    .on("mouseout", function () {
                        let size = d3.select(this).attr('r')

                        d3.select(this)
                            .style("fill", "red")
                            .attr("r", size * 10 / 13);
                    })
                    .append("title")
                    .text(function (d) {
                        return d.station_name + ", " + d.region;
                    });

                createList(data);
            }
        );
}

function createList(data) {
    const list = d3.select("#list")
        .append("ul");

    list.selectAll("li")
        .data(data)
        .enter()
        .append("li")
        .append("a")
        .attr("href", d => {
            return window.location.origin + '/station/' + d.id;
        })
        .attr("id", function (d) {
            return d.id;
        })
        .text(function (d) {
            return d.station_name + ', ' + d.region;
        })
        .style("color", "black")
        .style("text-decoration", "none")
        .on("mouseover", function (d) {
            const listItem = d3.select(this)
                .style("cursor", "pointer")
                .style("background-color", "lightgray")
                .style("font-weight", "bold");

            let circle = g.selectAll("circle")
                .filter(function (e) {
                    return e.id === listItem.attr("id");
                });

            let size = circle.attr('r');

            circle
                .style("fill", "lightgreen")
                .attr("r", size * 1.3);
        })
        .on("mouseout", function (d) {
            const listItem = d3.select(this)
                .style("background-color", "white")
                .style("font-weight", "normal");

            let circle = g.selectAll("circle")
                .filter(function (e) {
                    return e.id === listItem.attr("id");
                });

            let size = circle.attr('r');

            circle
                .style("fill", "red")
                .attr("r", size * 10 / 13);
        });
}
