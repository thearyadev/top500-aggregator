
const hero_color_data = $("colors").data().herocolors


function drawHeroTrendChartAllRegions() {
    const chartElement = $('#T_ALL_ALL')
    const data = $('data').data().trends
    const seasons = JSON.parse($('seasons').data().seasons.replace(/'/g, '"')).map(item => item.split("_")[0])



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







    series: data.map(item => {
    console.log(item)
     return {
        color: lookup_hero_color(item.name),
        ...item
        }
    }),
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
let lastWidth = window.innerWidth;

window.addEventListener('resize', function () { // redraw charts on resize
    const currentWidth = window.innerWidth;
    if (currentWidth !== lastWidth) {

        $('#T_ALL_ALL').empty()
        lastWidth = currentWidth
        drawHeroTrendChartAllRegions()
    }

});

function lookup_hero_color(name){
    return hero_color_data[name] || "black"
}