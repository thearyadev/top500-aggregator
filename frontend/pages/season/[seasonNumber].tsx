import {useRouter} from "next/router";
import {Card} from "@/app/components";
import {BarChart} from "@/app/components";
import {GetServerSidePropsContext} from "next";

type Statistic = {
    mean: number;
    standard_deviation: number;
    variance: number;
}

type BarChartData = {
    labels: string[];
    values: number[];
}

type SingleChart = {
    graph: BarChartData;
    statistic: Statistic;
}

type SeasonData = {
    [key: string]: SingleChart;
}


const Season = ({data, season_list}: { data: SeasonData, season_list: string[]}) => {
    return (
        <>
            <Card title="Hero Occurrences: All Slots" nowrap>
                {Object.keys(data).map(key => {
                    if (key.includes("O_ALL")){
                        const [_, role, region] = key.split("_")
                        return <BarChart title={`${region}`} graph={data[key].graph} maxY={region === "ALL" ? 1250 : 500 } />
                    }
                })}
            </Card>



            <Card title="Hero Occurrences: First Most Played">
                {Object.keys(data).map(key => {
                    if (key.includes("OFMP")){
                        const [_, role, region] = key.split("_")
                        return <BarChart title={`${role}: ${region}`} graph={data[key].graph} maxY={region === "ALL" ? 500 : 300 } />
                    }
                })}

            </Card>

            <Card title="Hero Occurrences: Second Most Played">
                {Object.keys(data).map(key => {
                    if (key.includes("OSMP")){
                        const [_, role, region] = key.split("_")
                        return <BarChart title={`${role}: ${region}`} graph={data[key].graph} maxY={region === "ALL" ? 500 : 300 } />
                    }
                })}

            </Card>


            <Card title="Hero Occurrences: Third Most Played">
                {Object.keys(data).map(key => {
                    if (key.includes("OTMP")){
                        const [_, role, region] = key.split("_")
                        return <BarChart title={`${role}: ${region}`} graph={data[key].graph} maxY={region === "ALL" ? 500 : 300 } />
                    }
                })}

            </Card>

        </>
    )
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
    // @ts-ignore
    const {seasonNumber} = context.params;

    // Make an API call using seasonNumber
    const res = await fetch(`http://web:8000/chart/${seasonNumber}_8`);
    const data = await res.json();


    const res2 = await fetch("http://web:8000/d/seasons")
    const season_list = await res2.json()

    return {
        props: {
            data,
            season_list,
        },
    };
}


export default Season