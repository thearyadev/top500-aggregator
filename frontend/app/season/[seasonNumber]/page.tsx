import React from "react";
import { Card } from "@/app/components";
import {
  fetchSingleSeasonPageChartData,
  fetchSingleSeasonStdDevs,
} from "@/app/utils/serverSideProps";
import { BarChart } from "@/app/components";
import TopMatter from "@/app/components/topmatter/topmatter";

const HeroStdDev = ({ value, role }: { value: number; role: string }) => {
  return (
    <div className="text-center pt-5 pb-5">
      <h5>{role}</h5>
      <h6 className="text-lg text-center">
        {Math.round((value + Number.EPSILON) * 100) / 100}
      </h6>
    </div>
  );
};

const SeasonPage = async ({ params }: { params: { seasonNumber: string } }) => {
  const seasonChartData = await fetchSingleSeasonPageChartData(
    +params.seasonNumber,
  );
  const seasonStdDevs = await fetchSingleSeasonStdDevs(+params.seasonNumber);

  return (
    <main>
      <TopMatter seasonNumber={params.seasonNumber} />
      <Card
        title="Role Standard Deviation: All Slots, All Regions"
        subtitle={
          "Note: The standard deviation is calculated with the 10th percentile excluded. T500 aggregator by nature skews the accuracy of the low outliers in a data set. For this reason, the bottom 10% of entries for any given set (support, damage or tank) is excluded from the calculation."
        }
      >
        <HeroStdDev value={seasonStdDevs.SUPPORT} role={"SUPPORT"} />
        <HeroStdDev value={seasonStdDevs.DAMAGE} role={"DAMAGE"} />
        <HeroStdDev value={seasonStdDevs.TANK} role={"TANK"} />
      </Card>

      <Card title="Hero Occurrences: All Slots" nowrap>
        {Object.keys(seasonChartData).map((key) => {
          if (key.includes("O_ALL")) {
            const [_, role, region] = key.split("_");
            return (
              <BarChart
                title={`${region}`}
                graph={(seasonChartData as any)[key].graph}
                maxY={region === "ALL" ? 1250 : 500}
              />
            );
          }
        })}
      </Card>

      <Card title="Hero Occurrences: First Most Played">
        {Object.keys(seasonChartData).map((key) => {
          if (key.includes("OFMP")) {
            const [_, role, region] = key.split("_");
            return (
              <BarChart
                title={`${role}: ${region}`}
                graph={(seasonChartData as any)[key].graph}
                maxY={region === "ALL" ? 500 : 300}
              />
            );
          }
        })}
      </Card>

      <Card title="Hero Occurrences: Second Most Played">
        {Object.keys(seasonChartData).map((key) => {
          if (key.includes("OSMP")) {
            const [_, role, region] = key.split("_");
            return (
              <BarChart
                title={`${role}: ${region}`}
                graph={(seasonChartData as any)[key].graph}
                maxY={region === "ALL" ? 500 : 300}
              />
            );
          }
        })}
      </Card>

      <Card title="Hero Occurrences: Third Most Played">
        {Object.keys(seasonChartData).map((key) => {
          if (key.includes("OTMP")) {
            const [_, role, region] = key.split("_");
            return (
              <BarChart
                title={`${role}: ${region}`}
                graph={(seasonChartData as any)[key].graph}
                maxY={region === "ALL" ? 500 : 300}
              />
            );
          }
        })}
      </Card>
    </main>
  );
};

export default SeasonPage;
