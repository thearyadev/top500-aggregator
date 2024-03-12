import React from "react";
import { LineChart } from "../components";
import { Card } from "../components";
import TopMatter from "../components/topmatter/topmatter";
import { get_occurrence_trend_lines, get_season_list, get_std_deviation_trend_lines } from "../server/actions";

const TrendsPage = async () => {
    const seasonalOccurrencesTrend = await get_occurrence_trend_lines()
    const seasonalStdDevTrend = await get_std_deviation_trend_lines() 
    const seasonList = await get_season_list()

    return (
        <main>
            <TopMatter seasonNumber="trends" />
            <Card title={"Seasonal Trends"} nowrap>
                <LineChart
                    data={seasonalOccurrencesTrend}
                    seasons={seasonList}
                    title={"Occurrences: All Roles All Regions"}
                    className=""
                />
                <LineChart
                    data={seasonalStdDevTrend}
                    seasons={seasonList}
                    title={"Standard Devation: By Role All Regions"}
                    className=""
                />

            </Card>

        </main>
    );
};
export default TrendsPage;
