"use client";

import * as Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import { useRef, useState } from "react";
import { HeroColors } from "@/app/components/charts/heroColors";
import type { TrendLine } from "@/app/utils/serverSideProps";
import classNames from "classnames";

interface LineChartProps extends HighchartsReact.Props {
  title: string;
  data: TrendLine[];
  seasons: string[];
  className: string;
}

const LineChart = (props: LineChartProps) => {
  const { data, seasons, title } = props;
  const options: Highcharts.Options = {
    title: {
      // @ts-ignore
      text: null,
      margin: 0,
    },
    xAxis: {
      categories: seasons,
      min: 0,
      max: 9,
    },
    series: data.map((item) => ({
      color: HeroColors[item.name] ?? null,
      type: "line",
      ...item,
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
        pointPlacement: "on",
        label: {
          connectorAllowed: false,
        },
      },
    },
    chart: {
      height: "45%",
      events:{
        load: () => {setLoading(false)}
      }
    },
  };
  const chartComponentRef = useRef<HighchartsReact.RefObject>(null);
  const [loading, setLoading] = useState(true)
  return (
    <div className={props.className}>
      <h5 className="text-center pb-2">{title}</h5>

      <div className={loading ? "hidden" : ""}>
        <HighchartsReact
          id="gnomegnome"
          highcharts={Highcharts}
          options={options}
          ref={chartComponentRef}
          {...props}
        />

      </div>

      <div role="status" className={`max-w flex text-center justify-center items-center h-[60rem]  animate-pulse ${loading ? '' : "hidden"}`}>
        <p>Loading...</p>
      </div>
    </div>
  );
};

export default LineChart;
