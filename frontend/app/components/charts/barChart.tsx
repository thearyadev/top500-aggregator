"use client";

import * as Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import { useEffect, useRef, useState } from "react";
import styles from "./barChart.module.scss";
import { HeroColors } from "@/app/components/charts/heroColors";
import classNames from "classnames";
import { BarChartData } from "@/app/server/actions";
import pareto from "highcharts/modules/pareto";
import { IconPercentage30 } from "@tabler/icons-react";
import { Loader } from "@mantine/core";

if (typeof Highcharts === "object") {
    pareto(Highcharts);
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
    const numbersWithIndices: [number, number][] = numbers.map(
        (value, index) => [index, value],
    );
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
    const mean =
        graph.values.reduce((sum, num) => sum + num, 0) / graph.values.length;

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
            plotLines: [
                {
                    color: "red",
                    width: 2,
                    value: findParetoIndex(graph.values) + 0.5,
                    zIndex: 10,
                    label: {
                        text: "Pareto Index - 80%",
                    },
                },
            ],
        },
        series: [
            {
                type: "pareto",
                baseSeries: 1,
                zIndex: 11,
            },
            {
                type: "column",
                name: "Occurrences",
                data: graph.values.map((item, index) => {
                    return {
                        y: Math.round(item),
                        color: HeroColors[graph.labels[index]],
                    }; // do lookup
                }),
                dataLabels: {
                    enabled: true,
                    align: "center",
                    zIndex: 0,
                },
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
                    value: mean,
                    label: {
                        text: "Mean",
                        textAlign: "center",
                    },
                },
            ],
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
    );
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
                {/* Statistics Panel */}
                <div className="mt-3 p-3 bg-gray-50 rounded-lg shadow-sm border border-gray-200">
                    <div className="grid grid-cols-3 gap-3 text-center">
                        <div className="stat-item">
                            <div className="text-xs text-gray-500 font-medium">
                                Gini Coefficient
                            </div>
                            <div
                                className={`
                        text-lg font-semibold
                        ${
                            props.giniCoefficient < 0.3
                                ? "text-green-500"
                                : props.giniCoefficient < 0.45
                                  ? "text-amber-500"
                                  : "text-red-500"
                        }
                    `}
                            >
                                {props.giniCoefficient.toFixed(2)}
                            </div>
                        </div>
                        <div className="stat-item">
                            <div className="text-xs text-gray-500 font-medium">
                                Mean
                            </div>
                            <div className="text-lg font-semibold">
                                {mean.toFixed(2)}
                            </div>
                        </div>
                        <div className="stat-item group relative">
                            <div className="text-xs text-gray-500 font-medium flex items-center justify-center">
                                Data Points
                                <span className="ml-1 cursor-help">
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        className="h-3.5 w-3.5 text-gray-400"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                    >
                                        <path
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                            strokeWidth={2}
                                            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                                        />
                                    </svg>
                                </span>
                            </div>
                            <div className="text-lg font-semibold">
                                {props.graph.values
                                    .reduce((a, v) => a + v, 0)
                                    .toFixed(0)}
                            </div>
                            <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-48 p-2 bg-gray-800 text-white text-xs rounded shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity duration-200 z-10">
                                This count has "Blanks" removed, so it may not
                                reflect the expected value for this chart.
                                <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-gray-800"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div
                role="status"
                className={`max-w flex text-center justify-center items-center h-[18rem] animate-pulse ${loading ? "" : "hidden"}`}
            >
                <Loader color="blue" className="text-blue-500" />
            </div>
        </div>
    );
};

export default BarChart;
