import React from "react";
import { LineChart } from "../components";
import { Card } from "../components";
import TopMatter from "../components/topmatter/topmatter";
import {
    get_occurrence_trend_lines,
    get_season_list,
    get_std_deviation_trend_lines,
} from "../server/actions";

const TrendsPage = async () => {
    const seasonalOccurrencesTrend = await get_occurrence_trend_lines();
    const seasonalOccurrencesTrendWeighted = await get_occurrence_trend_lines(true);
    const seasonalStdDevTrend = await get_std_deviation_trend_lines();
    const seasonList = await get_season_list();

    return (
        <main>
            <TopMatter seasonNumber="trends" />
            <Card title={"Seasonal Trends"} nowrap>
                <LineChart
                    data={seasonalOccurrencesTrendWeighted}
                    seasons={seasonList}
                    title={"Occurrences: All Roles All Regions (Weighted)"}
                    className=""
                />
                <LineChart
                    data={seasonalOccurrencesTrend}
                    seasons={seasonList}
                    title={"Occurrences: All Roles All Regions (Raw)"}
                    className=""
                />
                <LineChart
                    subtitle="The Gini Coefficient is a measure of inequality. A higher value indicates greater inequality. A value approaching 0 indicated perfect quality. For example, [1, 1, 1, 1] = 0. This calculation is made with the 10th percentile excluded. The nature of top 500 means that the lesser picked heroes are disproportionately picked, and therefore heavily skew the data."
                    data={seasonalStdDevTrend}
                    seasons={seasonList}
                    title={"Gini Coefficient: By Role All Regions, First Most Played"}
                    className=""
                />
            </Card>
        </main>
    );
};
export default TrendsPage;
