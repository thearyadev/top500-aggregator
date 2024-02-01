import React from "react";
import {
    fetchSeasonList,
    fetchSeasonalOccurrenceTrend,
    fetchSeasonalStdDevTrendByRole,
} from "../utils/serverSideProps";
import { LineChart } from "../components";
import { Card } from "../components";
import TopMatter from "../components/topmatter/topmatter";

const TrendsPage = async () => {
    const seasonalOccurrencesTrend = await fetchSeasonalOccurrenceTrend();
    const seasonalStdDevTrend = await fetchSeasonalStdDevTrendByRole();
    const seasonList = await fetchSeasonList()

    return (
        <main>
            <TopMatter seasonNumber="trends" />
            <Card title={"Seasonal Trends"} nowrap>
                <LineChart
                    data={seasonalOccurrencesTrend}
                    seasons={seasonList}
                    title={"Occurrences: All Roles All Regions"}
                    className="min-h-[60rem]"
                />
                <LineChart
                    title={"Standard Deviation: By Role All Regions"}
                    data={seasonalStdDevTrend}
                    seasons={seasonList}
                    className="min-h-[60rem]"
                />
            </Card>
        </main>
    );
};
export default TrendsPage;
