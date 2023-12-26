import Season from "@/pages/season/[seasonNumber]";
import {
    fetchSeasonList,
    fetchSingleSeasonPageChartData,
    fetchSingleSeasonStdDevs,
    SeasonData,
    StdDevs
} from "@/app/utils/serverSideProps";
import {GetServerSidePropsContext} from "next";

const Index = ({seasonChartData, seasonStdDevs}: {seasonChartData: SeasonData, seasonStdDevs: StdDevs}) => {
    return <Season seasonChartData={seasonChartData} seasonStdDevs={seasonStdDevs} />
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
    // @ts-ignore
    const seasonList = await fetchSeasonList()
    const seasonNumber = Number(seasonList[seasonList.length -1].split("_")[0])
    const seasonChartData = await fetchSingleSeasonPageChartData(seasonNumber)
    const seasonStdDevs = await fetchSingleSeasonStdDevs(seasonNumber)

    return {
        props: {
            seasonChartData,
            seasonStdDevs
        },
    };
}



export default Index