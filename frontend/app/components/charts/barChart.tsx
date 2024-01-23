"use client";

import * as Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import { useRef } from "react";
import styles from "./barChart.module.scss";
import { HeroColors } from "@/app/components/charts/heroColors";
import classNames from "classnames";

interface GraphData {
  labels: string[];
  values: number[];
}

interface BarChartProps extends HighchartsReact.Props {
  title: string;
  graph: GraphData;
  maxY: number;
  className?: string | string[]
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
  };
  const chartComponentRef = useRef<HighchartsReact.RefObject>(null);
  const chartContainerStyle = classNames(styles.chartContainer, props.className)
  return (
    <div className={chartContainerStyle}>
      <h5 className="text-center pb-2 capitalize">{title.toLowerCase()}</h5>
      <HighchartsReact
        id="gnomegnome"
        highcharts={Highcharts}
        options={options}
        ref={chartComponentRef}
        {...props}
      />
    </div>
  );
};

export default BarChart;
