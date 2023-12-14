function drawHeroTrendChartAllRegions() {
    const chartElement = $('#T_ALL_ALL')
    const data = $('data').data().trends
    const seasons = JSON.parse($('seasons').data().seasons.replace(/'/g, '"')).map(item => item.split("_")[0])
    console.log(seasons)
    // const xAxisLabels = Object.keys(data.map(item => item.split("_")[0])



Highcharts.chart('T_ALL_ALL', {
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },
    xAxis: {
        categories:  seasons,
        min: 0, // Replace with your actual minimum value
        max: seasons.length -1, // Replace with your actual maximum value
        startOnTick: false,
        endOnTick: false,
    },
    plotOptions: {
        series: {
            pointPadding: 0,
            groupPadding: 0,
            pointPlacement: 'on',
            label: {
                connectorAllowed: false
            }
        },
    },







    series: data,
    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }

});

}

drawHeroTrendChartAllRegions()

window.addEventListener('resize', function () { // redraw charts on resize
    $('#T_ALL_ALL').empty()
    drawHeroTrendChartAllRegions()
});

