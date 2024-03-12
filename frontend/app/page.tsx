import SeasonPage from "./season/[seasonNumber]/page";
import { get_season_list } from "./server/actions";

const IndexPage = async () => {
    const latestSeason = (await get_season_list()).reverse()[0];
    return <SeasonPage params={{ seasonNumber: latestSeason }} />;
};

export default IndexPage;
