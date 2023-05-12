const data = $(`data`).data().trends;
console.log(data)
const charts = [
    "SUPPORT",
    "DAMAGE",
    "TANK",
] // all chart ids

google.charts.load("current", { "packages": ['corechart'] })
google.charts.setOnLoadCallback(function () {
    charts.forEach(drawChart)
}) // once loaded, draw each chart



function drawChart(chartName) { // value is region. Americas, Europe, Asia, All
    const graphData = [
        ["Season"]
    ]; // first row of data is the season# and hero names


    for (let season in data) { // iter season number in data
        // for each season

        let specific_chart_data = data[season][chartName] // get the season data for the role (chartName) currently being iterated
        let season_data_to_add = ["S" + season.replace("_8", ""),] // this array is the NEXT row in graphData. This starts with the season number
        // this value is formatted to be readable. S1, S2, S3, etc.
        for (let hero in specific_chart_data) {
            // iter heroes
            if (!graphData[0].includes(data[season][chartName][hero]["hero"])) { // check if the hero exists in the graphData first row
                graphData[0].push(data[season][chartName][hero]["hero"]) // if not, add it
            }



            season_data_to_add.push(data[season][chartName][hero]["count"]) // add the heroes value (count) to the next row being added, which was initialized on line 26

        }
        graphData.push(season_data_to_add) // add the row to the graphData

    }

    var parsedGraphData = google.visualization.arrayToDataTable(graphData) // convert to datatable

    var chart = new google.visualization.LineChart(document.getElementById(chartName)); // init charts

    var options = {
        'chartArea': {
            'width': '80%',
            'height': '90%'
        },
        isStacked: "relative",
        theme: "material",
        fontName: 'Lato',





    }
    chart.draw(parsedGraphData, options) // draw
}




window.addEventListener('resize', function () { // redraw charts on resize

    charts.forEach((value) => {
        $(`#${value}`).empty()
    })

    charts.forEach(drawChart)
});