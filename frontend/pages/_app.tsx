// pages/_app.tsx
import '../app/globals.scss'; // Ensure this path is correct
import type {AppProps} from 'next/app';
import {Header} from "@/app/components";
import {useRouter} from "next/router";

function MyApp({Component, pageProps}: AppProps) {
    const links = [
        {label: "Season 1", path: "/season/1"},
        {label: "Season 2", path: "/season/2"},
        {label: "Season 3", path: "/season/3"},
        {label: "Season 4", path: "/season/4"},
        {label: "Season 5", path: "/season/5"},
        {label: "Season 6", path: "/season/6"},
        {label: "Season 7", path: "/season/7"},
        {label: "Season 8", path: "/season/8"},
        {label: "Season 9", path: "/season/9"},
        {label: "Season 10", path: "/season/10"},
        {label: "Season 11", path: "/season/11"},
        {label: "Season 12", path: "/season/12"},
        {label: "Season 13", path: "/season/13"},
        {label: "Season 14", path: "/season/14"},
        {label: "Trends", path: "/trends"},
    ]

    const router = useRouter()
    const {seasonNumber} = router.query

    return (
        <>
            <Header nav_links={links.reverse()}/>
            <main className="mt-5 lg:ml-3 lg:mr-3 sm:ml-1 sm:mr-1">
                <h2 className="text-4xl pb-4">Season {seasonNumber}</h2>
                <p className="pb-2"><strong>Welcome to Overwatch 2 Top 500 Aggregator</strong></p>

                <p>The data available on this page is not 100% accurate. Data collection involves computer vision and
                    image classification using a neural network, and as
                    such, there is a slight error rate. This error rate is most apparent in some charts where the
                    incorrect
                    role appears, such as a support chart containing Echo. More information on data collection is
                    available
                    on my <a href="https://github.com/thearyadev/top500-aggregator" target="_blank">GitHub</a> page.</p>

                <p className="pb-2"><strong>What is this data?</strong></p>
                <p>The data below is taken from the in-game top 500 leaderboards. The information available there
                    includes a single player's matches played and their top 3 heroes played. The charts and categories
                    below represent data for the hero "slot" in a top 500 leaderboard entry. For example, they count the
                    number of people who have Kiriko as their most played hero, or Widowmaker as their second most
                    played hero. The data is a high-level overview of what heroes are popular or unpopular and is by no
                    means an accurate representation of hero pick rates.</p>

                <p className="pb-2"><strong>When is the data updated?</strong></p>
                <p>The dataset is updated once per season. Starting in season 8, the most recent season will be updated
                    weekly, overwritten each week until the end of the season</p>
                <hr className="m-5" />

                <Component {...pageProps} />
            </main>
        </>

    )

}

export default MyApp;
