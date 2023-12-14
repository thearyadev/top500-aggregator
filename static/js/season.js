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

function map_multi_array(arrayOfObjects){
    const heroes = [];
    const counts = [];

    arrayOfObjects.forEach(item => {
        heroes.push(item.hero)
        counts.push(item.count)
    })
    return [heroes, counts]

}

function drawChart(chartName) {

    const chartElement = $(`#${chartName}`)
    const chartDataRaw = chartElement.data().graphdata
    const [heroes, counts] = map_multi_array(chartDataRaw.graph)
    const stats = chartDataRaw.statistic
    Highcharts.chart(chartName, {
        chart: {
            type: 'column'
        },
        xAxis: {
            categories: heroes,
            crosshair: true,
            accessibility: {
                description: 'Heroes'
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Occurrences'
            }
        },
        tooltip: {
            valueSuffix: ' Occurrences'
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [
            {
                name: `::`,
                data: counts
            },
        ]
    });


    chartElement.parent().append(`<p class='chart-stats small text-muted'><small>Mean: ${stats?.mean} | Variance: ${stats?.variance} | Standard Deviation: ${stats?.standard_deviation} | # Entires: ${counts.reduce((acc, cur) => acc + cur, 0)}</small></p>`)

}

let lastWidth = window.innerWidth;

window.addEventListener('resize', function () { // redraw charts on resize
    const currentWidth = window.innerWidth;
    if (currentWidth !== lastWidth) {
        charts.forEach((value) => {
            $(`#${value}`).empty()
            $(".chart-stats").remove()
        })
        lastWidth = currentWidth
        charts.forEach(drawChart)
    }

});

window.onload = () => {
    charts.forEach(drawChart)

}