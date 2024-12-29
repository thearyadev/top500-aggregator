"use client";

import * as Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import { useEffect, useRef, useState } from "react";
import styles from "./barChart.module.scss";
import { HeroColors } from "@/app/components/charts/heroColors";
import classNames from "classnames";
import { BarChartData } from "@/app/server/actions";
import pareto from 'highcharts/modules/pareto';
import { IconPercentage30 } from "@tabler/icons-react";
pareto(Highcharts)

interface BarChartProps extends HighchartsReact.Props {
    title: string;
    graph: BarChartData;
    maxY: number;
    giniCoefficient: number;
    className?: string | string[];
}
const BarChart = (props: BarChartProps) => {
    const { title, graph, maxY } = props;
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
            categories: graph.labels,
        },
        series: [
            {
                type: 'pareto',
                baseSeries: 1 // index of column series
            },
            {
                type: "column",
                name: "Occurrences",
                data: graph.values.map((item, index) => {
                    return { y: item, color: HeroColors[graph.labels[index]] }; // do lookup
                }),
            },
        ],
        credits: {
            enabled: false,
        },
        yAxis: {
            min: 0,
            max: maxY,
            title: {
                text: null,
            },
        },
        chart: {
            events: {
                load: () => {
                    setLoading(false);
                },
            },
        },
    };
    const chartComponentRef = useRef<HighchartsReact.RefObject>(null);
    const chartContainerStyle = classNames(
        styles.chartContainer,
        props.className,
    ); // meow
    const [loading, setLoading] = useState(true);
    return (
        <div className={chartContainerStyle}>
            <h5 className="text-center pb-2 capitalize">
                {title.toLowerCase()}
            </h5>
            <div className={loading ? "hidden" : ""}>
                <HighchartsReact
                    id="gnomegnome"
                    highcharts={Highcharts}
                    options={options}
                    ref={chartComponentRef}
                    {...props}
                />
                <div
                    className={`
        text-center text-sm pb-2 font-mono
        ${props.giniCoefficient < 0.15 ? 'text-green-500' :
                            props.giniCoefficient < 0.30 ? 'text-gray-500' :
                                'text-red-500'}
    `}
                >
                    Gini Coefficient: {props.giniCoefficient.toFixed(2)}
                </div>
            </div>

            <div
                role="status"
                className={`max-w flex text-center justify-center items-center h-[18rem]  animate-pulse ${loading ? "" : "hidden"}`}
            >
                <p>Loading...</p>
            </div>
        </div>
    );
};

export default BarChart;
