import { Spoiler } from "@mantine/core";
import Image from "next/image";
import Link from "next/link";

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

            <Spoiler hideLabel="Hide" showLabel="Read More">
                <p className="pb-2">
                    <strong>Welcome to Overwatch 2 Top 500 Aggregator</strong>
                </p>
                <p>
                    Top 500 aggregator is a data analysis tool to create
                    aggregations based on the Overwatch 2 top 500 leaderboards.
                    The site contains data from season 34 to present and primarily
                    counts the occurrences of a hero on the leaderboard.
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
                <Image src="images/leaderboard-diagram.png" alt="Leaderboard breakdown diagram" width="5000" height="5000" />
                <p className="pb-2">
                    <strong>When is the data updated?</strong>
                </p>
                <p>The dataset is updated at irregular intervals throughout the season,
                    overwriting the previous one. Once the end of the season has been reached,
                    the data will be updated once again and will then be a permanent season in the database.
                </p>

                <p className="pb-2">
                    <strong>How is the data collected?</strong>
                </p>
                <p>
                    Data collection begins in game, where a script takes screenshots
                    of each page of the top 500 leaderboards. Each image is categorized
                    based on the role and region.

                    Then the images are processed by another script, which crops them and
                    extracts the hero image from the full leaderboard screenshot. Once complete,
                    the images are compared with a local set of known images. This is done by calculating
                    a hash ("dhash") on the known image and the unknown image. With the two hashes,
                    you can determine its hamming distance. The unknown image is hashed and compared to all
                    known images. The results are then sorted ascending, and the lowest value is determined
                    to be the correct hero.
                </p>

                <p className="pb-2">
                    <strong>How accurate is this information?</strong>
                </p>
                <p className="pb-1">
                    Theres two components to this question. The accuracy of the data generation,
                    and the amount of value the data has in the world.
                </p>

                <p className="pb-1">

                    From my testing, the data is 100% accurate. In the Github repository you will find a benchmarking tool which allows me to performance test the comparison on actual leaderboard images. Currently, it completes 130 tests on 13 images from the leaderboard which have been manually classified. The result is an accuracy is 100%. Realistically, I can't determine if the accuracy is actually 100%. The comparison method is exceptionally good at static image comparison, but there could be flaws in the system as a whole that I'm not aware of.
                </p>
                <p>
                    The amount of value this data has when actually evaluating the game is debatable. Top 500 may not be an accurate representation of the state of the game. This is because only the top 3 heroes are visible to the user. That being said, the most popular heroes will be very accurate, and the trends over time will be very accurate, but the validity of results from a hero like Junkrat which has a small handful of "junkrat mains" that would ever have junkrat become their most played hero, junkrat is disproportinatly misrepresented in this dataset.

                </p>



            </Spoiler>
            <hr className="m-5" />
        </div >
    );
};

export default TopMatter;
