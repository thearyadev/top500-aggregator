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
import { Loader } from "@mantine/core";

if (typeof Highcharts === 'object') {
    pareto(Highcharts)
}

interface BarChartProps extends HighchartsReact.Props {
    title: string;
    graph: BarChartData;
    maxY: number;
    giniCoefficient: number;
    className?: string | string[];
}
function findParetoIndex(numbers: number[], percentage: number = 0.8): number {
    const totalSum = numbers.reduce((sum, num) => sum + num, 0);
    const targetSum = totalSum * percentage;
    const numbersWithIndices: [number, number][] = numbers.map((value, index) => [index, value]);
    numbersWithIndices.sort((a, b) => b[1] - a[1]);
    let cumulativeSum = 0;
    for (const [originalIndex, value] of numbersWithIndices) {
        cumulativeSum += value;
        if (cumulativeSum >= targetSum) {
            return originalIndex;
        }
    }

    return numbers.length - 1;
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
            plotLines: [{
                color: "red",
                width: 2,
                value: findParetoIndex(graph.values) + 0.5,
                zIndex: 10,
                label: {
                    text: "Pareto Index - 80%",
                }
            }]
        },
        series: [
            {
                type: 'pareto',
                baseSeries: 1,
                zIndex: 11
            },
            {
                type: "column",
                name: "Occurrences",
                data: graph.values.map((item, index) => {
                    return { y: Math.round(item), color: HeroColors[graph.labels[index]] }; // do lookup
                }),
                dataLabels: {
                    enabled: true,
                    align: 'center',
                    zIndex: 0
                }
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
            plotLines: [
                {
                    color: "red",
                    width: 2,
                    zIndex: 10,
                    value: graph.values.reduce((sum, num) => sum + num, 0) / graph.values.length,
                    label: {
                        text: "Mean",
                        textAlign: "center"
                    }
                }
            ]
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
        ${props.giniCoefficient < 0.30 ? 'text-green-500' :
                            props.giniCoefficient < 0.45 ? 'text-gray-500' :
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
                <Loader color="blue" className="text-blue-500"/>
            </div>
        </div>
    );
};

export default BarChart;
