import {GetServerSidePropsContext} from "next";
import {Card} from "@/app/components";
import {LineChart} from "@/app/components";
import type {TrendLine} from "@/app/utils/serverSideProps";
import {
    fetchSeasonalOccurrenceTrend,
    fetchSeasonList,
    fetchSeasonalStdDevTrendByRole,
} from "@/app/utils/serverSideProps";

const Trends = ({seasonalOccurrencesTrend, seasonalStdDevTrend, seasonList}: {
    seasonalOccurrencesTrend: TrendLine[],
    seasonalStdDevTrend: TrendLine[],
    seasonList: string[]
}) => {
    return (
        <>
            <Card title={"Seasonal Trends"} nowrap>
                <LineChart data={seasonalOccurrencesTrend} seasons={seasonList}
                           title={"Occurrences: All Roles All Regions"}/>
                <LineChart title={"Standard Deviation: By Role All Regions"} data={seasonalStdDevTrend}
                           seasons={seasonList}/>

            </Card>
        </>
    )
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
    const seasonalOccurrencesTrend = await fetchSeasonalOccurrenceTrend()
    const seasonList = await fetchSeasonList()
    const seasonalStdDevTrend = await fetchSeasonalStdDevTrendByRole()
    return {
        props: {
            seasonalOccurrencesTrend,
            seasonalStdDevTrend,
            seasonList
        },
    };
}


export default Trends;
