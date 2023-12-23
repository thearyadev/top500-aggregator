import {GetServerSidePropsContext} from "next";
import {Card} from "@/app/components";
import {LineChart} from "@/app/components";

export type TrendLine = {
    name: string;
    data: number[]
}


const Trends = ({data, season_list}: {data: TrendLine[], season_list: string[]}) => {
    return (
        <>
       <Card title={"Seasonal Trends"} nowrap>
           <LineChart data={data} seasons={season_list} title={"Occurrences: All Roles All Regions"} />
       </Card>
        </>
    )
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
    const res = await fetch(`http://localhost:7771/chart/trend/d`);
    const data = await res.json();


    const res2 = await fetch("http://localhost:7771/d/seasons")
    const season_list = await res2.json()

    return {
        props: {
            data,
            season_list,
        },
    };
}


export default Trends;