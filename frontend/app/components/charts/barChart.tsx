import * as Highcharts from 'highcharts';
import HighchartsReact from "highcharts-react-official";
import {useRef} from "react";
import styles from "./barChart.module.scss"
import {HeroColors} from "@/app/components/charts/heroColors";


interface BarChartProps extends HighchartsReact.Props {
    title: string;
    chartLabels: string[];
    chartValues: number[];
    maxY: number;
}


const BarChart = (props: BarChartProps) => {
    const {title, chartLabels, chartValues, maxY} = props;
    const options: Highcharts.Options = {
        title: {
            // @ts-ignore
            text: null,
            margin: 0,
        },
        legend: {
            enabled: false,
        },
        xAxis: {
            categories: chartLabels,
        },
        series: [{
            type: 'column',
            name: "Occurrences",
            data: chartValues.map((item, index) => {
                return {y: item, color: HeroColors[chartLabels[index]]} // do lookup
            })
        }],
        credits: {
            enabled: false,
        },
        yAxis: {
            min: 0,
            max: maxY,
            title: {
                text: null,
            },
        }
    };
    const chartComponentRef = useRef<HighchartsReact.RefObject>(null)

    return (
        <div className={styles.chartContainer}>
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

export default BarChart;