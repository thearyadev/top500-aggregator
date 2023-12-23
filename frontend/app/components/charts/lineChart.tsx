import * as Highcharts from 'highcharts';
import HighchartsReact from "highcharts-react-official";
import {useRef} from "react";
import {HeroColors} from "@/app/components/charts/heroColors";
import type {TrendLine} from "@/pages/trends";



interface LineChartProps extends HighchartsReact.Props {
    title: string;
    data: TrendLine[]
    seasons: string[]
}


const LineChart = (props: LineChartProps) => {
    const {data, seasons, title} = props;
    console.log(data)
    const options: Highcharts.Options = {
        title: {
            // @ts-ignore
            text: null,
            margin: 0,
        },
        xAxis: {
            categories: seasons,
            min: 0,
            max: 9
        },
        series: data.map(item => ({
            color: HeroColors[item.name],
            type: "line",
            ...item
        })),
        credits: {
            enabled: false,
        },
        yAxis: {
            title: {
                text: null,
            },
        },
        plotOptions: {
            series: {
                pointPlacement: 'on',
                label: {
                    connectorAllowed: false
                }
            },
        },
        chart: {
            height: "45%"
        }
    };
    const chartComponentRef = useRef<HighchartsReact.RefObject>(null)

    return (
        <div >
            <h5 className="text-center pb-2">{title}</h5>
            <HighchartsReact
                id="gnomegnome"
                highcharts={Highcharts}
                options={options}
                ref={chartComponentRef}
                {...props}
            />

        </div>

    )

}

export default LineChart;