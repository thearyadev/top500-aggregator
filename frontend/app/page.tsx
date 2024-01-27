import SeasonPage from "./season/[seasonNumber]/page";
import { fetchSeasonList } from "./utils/serverSideProps";

const IndexPage = async () => {
    const latestSeason = (await fetchSeasonList()).reverse()[0];
    return (
        <SeasonPage params={{ seasonNumber: latestSeason }} />
    );
};

export default IndexPage;
