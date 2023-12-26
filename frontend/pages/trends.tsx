import {GetServerSidePropsContext} from "next";
import {Card} from "@/app/components";
import {LineChart} from "@/app/components";

export type TrendLine = {
    name: string;
    data: number[]
}


const Trends = ({data, season_list, std_dev_data}: {data: TrendLine[], season_list: string[], std_dev_data: TrendLine[]}) => {
    return (
        <>
       <Card title={"Seasonal Trends"} nowrap>
           <LineChart data={data} seasons={season_list} title={"Occurrences: All Roles All Regions"} />
                       <LineChart title={"Standard Deviation: By Role All Regions"} data={std_dev_data} seasons={season_list} />

       </Card>
        </>
    )
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
    const res = await fetch(`http://server:8000/chart/trend/d`);
    const data = await res.json();


    const res2 = await fetch("http://server:8000/d/seasons")
    const season_list = await res2.json()

    const res3 = await fetch("http://server:8000/d/all_seasons_std_by_role")
    const std_dev_data = await res3.json()

    return {
        props: {
            data,
            season_list,
            std_dev_data,
        },
    };
}


export default Trends;
