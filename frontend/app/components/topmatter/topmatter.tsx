const TopMatter = ({
    seasonNumber,
    disclaimer,
}: {
    seasonNumber: string;
    disclaimer?: string;
}) => {
    let indicator = "";
    if (seasonNumber == "trends") {
        indicator = "Trends";
    } else {
        indicator = `Season: ${seasonNumber}`;
    }

    return (
        <div className="mt-5 lg:ml-3 lg:mr-3 sm:ml-1 sm:mr-1">
            <h1 className="text-3xl pb-4">{indicator}</h1>

            {disclaimer ? (
                <p className="text-red-500">
                    <span className="font-bold">DISCLAIMER: </span>
                    {disclaimer}
                </p>
            ) : undefined}
            <p className="pb-2">
                <strong>Welcome to Overwatch 2 Top 500 Aggregator</strong>
            </p>
            <p>
                The data available on this page is not 100% accurate. Data
                collection involves computer vision and image classification
                using a neural network, and as such, there is a slight error
                rate. This error rate is most apparent in some charts where the
                incorrect role appears, such as a support chart containing Echo.
                More information on data collection is available on my{" "}
                <a
                    href="https://github.com/thearyadev/top500-aggregator"
                    target="_blank"
                >
                    GitHub
                </a>{" "}
                page.
            </p>
            <p className="pb-2">
                <strong>What is this data?</strong>
            </p>
            <p>
                The data below is taken from the in-game top 500 leaderboards.
                The information available there includes a single player's
                matches played and their top 3 heroes played. The charts and
                categories below represent data for the hero "slot" in a top 500
                leaderboard entry. For example, they count the number of people
                who have Kiriko as their most played hero, or Widowmaker as
                their second most played hero. The data is a high-level overview
                of what heroes are popular or unpopular and is by no means an
                accurate representation of hero pick rates.
            </p>
            <p className="pb-2">
                <strong>When is the data updated?</strong>
            </p>
            <p>The dataset is updated once per season.</p>
            <hr className="m-5" />
        </div>
    );
};

export default TopMatter;
