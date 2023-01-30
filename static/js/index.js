const GRAPHS = ['OFMP_SUPPORT_AMERICAS', 'OFMP_SUPPORT_EUROPE', 'OFMP_SUPPORT_ASIA', 'OFMP_DAMAGE_AMERICAS', 'OFMP_DAMAGE_EUROPE', 'OFMP_DAMAGE_ASIA', 'OFMP_TANK_AMERICAS', 'OFMP_TANK_EUROPE', 'OFMP_TANK_ASIA', 'OFMP_SUPPORT_ALL', 'OFMP_DAMAGE_ALL', 'OFMP_TANK_ALL', 'OSMP_SUPPORT_AMERICAS', 'OSMP_SUPPORT_EUROPE', 'OSMP_SUPPORT_ASIA', 'OSMP_DAMAGE_AMERICAS', 'OSMP_DAMAGE_EUROPE', 'OSMP_DAMAGE_ASIA', 'OSMP_TANK_AMERICAS', 'OSMP_TANK_EUROPE', 'OSMP_TANK_ASIA', 'OSMP_SUPPORT_ALL', 'OSMP_DAMAGE_ALL', 'OSMP_TANK_ALL', 'OTMP_SUPPORT_AMERICAS', 'OTMP_SUPPORT_EUROPE', 'OTMP_SUPPORT_ASIA', 'OTMP_DAMAGE_AMERICAS', 'OTMP_DAMAGE_EUROPE', 'OTMP_DAMAGE_ASIA', 'OTMP_TANK_AMERICAS', 'OTMP_TANK_EUROPE', 'OTMP_TANK_ASIA', 'OTMP_SUPPORT_ALL', 'OTMP_DAMAGE_ALL', 'OTMP_TANK_ALL', 'O_ALL_AMERICAS', 'O_ALL_EUROPE', 'O_ALL_ASIA', 'O_ALL_ALL', 'GP_ASIA', 'GP_AMERICAS', 'GP_EUROPE']
Chart.defaults.backgroundColor = '#D93F1E'
GRAPHS.forEach(
    function (graph) {
        (
            async function () {
                const element = $(`#${graph}`)

                const data = element.data()?.graphdata
                const graphData = data.graph
                const stats = data.statistic

                new Chart(
                    element,
                    {
                        type: 'bar',
                        data: {
                            labels: graphData.map(row => row['hero']),
                            datasets: [
                                {
                                    label: "",
                                    data: graphData.map(row => row['count']),
                                    backgroundColor: [
                                        'rgba(255, 99, 132, 0.2)',
                                        'rgba(255, 159, 64, 0.2)',
                                        'rgba(255, 205, 86, 0.2)',
                                        'rgba(75, 192, 192, 0.2)',
                                        'rgba(54, 162, 235, 0.2)',
                                        'rgba(153, 102, 255, 0.2)',
                                        'rgba(201, 203, 207, 0.2)'
                                    ],
                                    borderColor: [
                                        'rgb(255, 99, 132)',
                                        'rgb(255, 159, 64)',
                                        'rgb(255, 205, 86)',
                                        'rgb(75, 192, 192)',
                                        'rgb(54, 162, 235)',
                                        'rgb(153, 102, 255)',
                                        'rgb(201, 203, 207)'
                                    ],
                                    borderWidth: 1
                                }
                            ]
                        },
                        fill: false,

                        options: {
                            plugins:{
                                legend: {
                                    display: false
                                },
                                subtitle: {
                                    display: true,
                                    text: `Mean: ${stats.mean} | Variance: ${stats.variance} | Standard Deviation: ${stats.standard_deviation}`,
                                    fullSize: true
                                }
                            },

                        }
                    }
                );
            }
        )();
    }
)