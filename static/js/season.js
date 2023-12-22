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

const chartCache = {}


const hero_color_data = $("colors").data().herocolors
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
    if (!chartCache.hasOwnProperty(chartName)){ // chart not in cache
        const chartElement = $(`#${chartName}`)

        const chartDataRaw = chartElement.data().graphdata
        const [heroes, counts] = map_multi_array(chartDataRaw.graph)
        const stats = chartDataRaw.statistic
        const entries = counts.reduce((acc, cur) => acc + cur, 0)
        const chartTypeBreakdown = chartName.split("_")
        let yAxisLength = 300; // standard size for all single role single region charts
        if (chartName === "O_ALL_ALL"){ // o type, all roles, all regions
            yAxisLength = 1250
        }else if (chartTypeBreakdown[chartTypeBreakdown.length - 1] === "ALL" || chartTypeBreakdown[0] === "O") { // all roles, single region or O-type chart
            yAxisLength = 500
        }

        chartCache[chartName] = {
            heroes, counts, stats, entries, yAxisLength, chartElement
        }

    }


    const chartDataCached = chartCache[chartName]
    Highcharts.chart(chartName, {
        chart: {
            type: 'column',
            margin: [75, 50, 75, 50]
        },
        xAxis: {
            categories: chartDataCached.heroes,
            crosshair: true,
            accessibility: {
                description: 'Heroes'
            }
        },
        yAxis: {
            min: 0,
            max: chartDataCached.yAxisLength,
            title: {
                text: 'Occurrences'
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [
            {
                name: `Occurrences`,
                data: chartDataCached.counts.map((item, index) => {
                    return {
                        y: item,
                        color: lookup_hero_color(chartDataCached.heroes[index])
                        }
                })
            },
        ]
    });

    console.log(chartDataCached)
    chartDataCached.chartElement.parent().append(`<p class='chart-stats small text-muted'><small>Mean: ${chartDataCached?.stats.mean} | Variance: ${chartDataCached?.stats.variance} | Standard Deviation: ${chartDataCached?.stats.standard_deviation} | # Entires: ${chartDataCached.entries}</small></p>`)

}


function lookup_hero_color(name){
    return hero_color_data[name] || "black"
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