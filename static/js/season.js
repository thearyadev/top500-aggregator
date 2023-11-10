const charts = [ // define all chart ids here
    'OFMP_SUPPORT_AMERICAS',
    'OFMP_SUPPORT_EUROPE',
    'OFMP_SUPPORT_ASIA', 'OFMP_DAMAGE_AMERICAS',
    'OFMP_DAMAGE_EUROPE', 'OFMP_DAMAGE_ASIA',
    'OFMP_TANK_AMERICAS', 'OFMP_TANK_EUROPE',
    'OFMP_TANK_ASIA', 'OFMP_SUPPORT_ALL', 'OFMP_DAMAGE_ALL',
    'OFMP_TANK_ALL', 'OSMP_SUPPORT_AMERICAS',
    'OSMP_SUPPORT_EUROPE', 'OSMP_SUPPORT_ASIA',
    'OSMP_DAMAGE_AMERICAS', 'OSMP_DAMAGE_EUROPE',
    'OSMP_DAMAGE_ASIA', 'OSMP_TANK_AMERICAS',
    'OSMP_TANK_EUROPE', 'OSMP_TANK_ASIA', 'OSMP_SUPPORT_ALL',
    'OSMP_DAMAGE_ALL', 'OSMP_TANK_ALL', 'OTMP_SUPPORT_AMERICAS',
    'OTMP_SUPPORT_EUROPE', 'OTMP_SUPPORT_ASIA', 'OTMP_DAMAGE_AMERICAS',
    'OTMP_DAMAGE_EUROPE', 'OTMP_DAMAGE_ASIA', 'OTMP_TANK_AMERICAS',
    'OTMP_TANK_EUROPE', 'OTMP_TANK_ASIA', 'OTMP_SUPPORT_ALL',
    'OTMP_DAMAGE_ALL', 'OTMP_TANK_ALL', 'O_ALL_AMERICAS', 'O_ALL_EUROPE',
    'O_ALL_ASIA', 'O_ALL_ALL', 
]
google.charts.load("current", { "packages": ['corechart'] }) // load charts
google.charts.setOnLoadCallback(function () {
    charts.forEach(drawChart) // draw charts
});


function drawChart(value) {

    let styles = [
        "fill-color: #ff6384; fill-opacity: 0.1; stroke-color: #ff6384;",
        "fill-color: #ff9f40; fill-opacity: 0.1; stroke-color: #ff9f40;",
        "fill-color: #ffcd56; fill-opacity: 0.1; stroke-color: #ffcd56;",
        "fill-color: #4bc0c0; fill-opacity: 0.1; stroke-color: #4bc0c0;",
        "fill-color: #36a2eb; fill-opacity: 0.1; stroke-color: #36a2eb;",
        "fill-color: #9966ff; fill-opacity: 0.1; stroke-color: #9966ff;",
        "fill-color: #c9cbcf; fill-opacity: 0.1; stroke-color: #c9cbcf;",
    ] // this is used to define the rotating chart color scheme. 
    styles.push(...styles)
    styles.push(...styles)
    styles.push(...styles)
    styles.push(...styles)

    let countSum = 0;
    const graphContainer = $(`#${value}`) // get the graph container of the current iter
    const graphData = graphContainer.data().graphdata // get the graph data from the container
    const stats = graphData.statistic // get the stats from the graph data
    var table = [
        ["Hero", "Mean", "Standard Deviation", "Count", { role: "style" }], // conv to table
    ]
    for (var i = 0; i < graphData.graph.length; i++) {
        let current = graphData.graph[i]
        countSum += current.count
        table.push([current.hero, stats.mean, stats.standard_deviation, current.count, styles[i]]) // push to table
    }

    var data = google.visualization.arrayToDataTable(table) // convert to google data table


    var options = { // chart styles

        'chartArea': {
            'width': '85%'
        },
        hAxis: {
            slantedTextAngle: 75
        },

        legend: { position: 'none' },
        theme: "material",
        fontName: 'Lato',
        seriesType: "bars",
        series: {
            0: { type: "line" },
            1: { type: "line" }

        },
        tooltip: { isHtml: true },
    };

    var chart = new google.visualization.ComboChart(document.getElementById(value)); // draw chart
    chart.draw(data, options);
    // add stats to the bottom
    graphContainer.append(`<p class='small text-muted'><small>Mean: ${stats?.mean} | Variance: ${stats?.variance} | Standard Deviation: ${stats?.standard_deviation} | # Entires: ${countSum}</small></p>`)
}

window.addEventListener('resize', function () { // redraw charts on resize
    
    charts.forEach((value) => {
        $(`#${value}`).empty()
    })

    charts.forEach(drawChart)
});