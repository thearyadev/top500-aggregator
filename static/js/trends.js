const data = $(`data`).data().trends;
console.log(data)
const charts = [
    "SUPPORT",
    "DAMAGE",
    "TANK",
]

google.charts.load("current", { "packages": ['corechart'] })
google.charts.setOnLoadCallback(function () {
    charts.forEach(drawChart)
})



function drawChart(chartName) { // value is region. Americas, Europe, Asia, All
    const graphData = [
        ["Season"]
    ];


    for (let season in data) {
        // for each season

        let specific_chart_data = data[season][chartName]
        let season_data_to_add = ["S" + season.replace("_8", ""),]
        for (let hero in specific_chart_data) {
            if (!graphData[0].includes(data[season][chartName][hero]["hero"])) {
                graphData[0].push(data[season][chartName][hero]["hero"])
            }



            season_data_to_add.push(data[season][chartName][hero]["count"])
        }
        graphData.push(season_data_to_add)

    }

    var parsedGraphData = google.visualization.arrayToDataTable(graphData)

    var chart = new google.visualization.LineChart(document.getElementById(chartName));

    var options = {
        'chartArea': {
            'width': '80%',
            'height': '90%'
        },
        isStacked: "relative",
        theme: "material",
        fontName: 'Lato',
        




    }
    chart.draw(parsedGraphData, options)
}



function get_heroes(obj) {
    const heroes = []
    for (let hero of obj) {
        heroes.push(hero.hero)
    }
    return heroes
}


window.addEventListener('resize', function () { // redraw charts on resize
    
    charts.forEach((value) => {
        $(`#${value}`).empty()
    })

    charts.forEach(drawChart)
});