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

type StdDevs = {
    DAMAGE: number;
    SUPPORT: number;
    TANK: number;
}

const HeroStdDev = ({value, role}: {value: number, role: string}) => {
    return (
    <div className="text-center pt-5 pb-5">
        <h5>{role}</h5>
        <h6 className="text-lg text-center">{Math.round((value + Number.EPSILON) * 100) / 100}</h6>

    </div>
    )
}

const Season = ({data, season_list, std_devs}: { data: SeasonData, season_list: string[], std_devs: StdDevs}) => {
    return (
        <>
            <Card title="Role Standard Deviation: All Slots, All Regions" subtitle={"Note: The standard deviation is calculated with the 10th percentile excluded. T500 aggregator by nature skews the accuracy of the low outliers in a data set. For this reason, the bottom 10% of entries for any given set (support, damage or tank) is excluded from the calculation."}>
                <HeroStdDev value={std_devs.SUPPORT} role={"SUPPORT"} />
                <HeroStdDev value={std_devs.DAMAGE} role={"DAMAGE"}/>
                <HeroStdDev value={std_devs.TANK} role={"TANK"}/>
            </Card>

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
    const res = await fetch(`http://server:8000/chart/${seasonNumber}_8`);
    const data = await res.json();


    const res2 = await fetch("http://server:8000/d/seasons")
    const season_list = await res2.json()

    const res3 = await fetch(`http://server:8000/d/single_season_std_by_role/${seasonNumber}_8`)
    const std_devs = await res3.json()

    return {
        props: {
            data,
            season_list,
            std_devs
        },
    };
}


export default Season