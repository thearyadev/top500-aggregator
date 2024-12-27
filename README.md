# Overwatch 2: Top 500 Aggregator
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fthearyadev%2Ftop500-aggregator.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fthearyadev%2Ftop500-aggregator?ref=badge_shield)

https://t500-aggregator.aryankothari.dev/

T500 Aggregator is a suite of tools and a web service to collect and display data on the Overwatch 2 Top 500 leaderboards. 

## Data Collection
Data is collected from the Overwatch 2 leaderboards directly. This data is then processed by a hashing algorithm called ("dhash")[https://en.wikipedia.org/wiki/Locality-sensitive_hashing]. Each hero present in a single leaderboard image is hashed and compared using a hamming distance comparison algorithm to determine its similarity to a known asset of a hero. 

The data is stored in the `./data` directory within the reposiroty.

## Data Integrity

The final processed dataset has a 100% accuracy to what is observed. This analysis is done by running the comparison algorithm on benchmarks, which can be found in the `./assets/benchmark/` directory. 

These benchmarks are updated regularly to identify changes in the leaderboard images, as well as to performance test the impact of adding a new hero. 

It is possible that the data is not 100% accurate, as I'm unable to fully verify each hero scanned to its actual counterpart. 

## Data Value

The leaderboards provide a snapshot of the heroes that are being played in the game. More specifically, it shows you the top 3 heroes for any given player. This prevents you from truely understanding the pickrates of a hero. 

However, the actual data can be approximated. 

### Approximating Pickrates -> Weighted Values
For example, given a player with 3 top hero playtime, you can approximate the second and third most played heroes as a percentage of the most played hero. These values can be found in `./frontend/app/server/actions.ts`. The weights are determined by scraping the public top 500 profiles and determining an estimation of the actual ratios. A sample size of 280, spanning all regions and seasons up to season 14 is used for this calculation. 

In a normal scenario, the top 3 would each recieve a full point. So in a chart, a player with Juno as their most played, would account for 1 entry, and another player with Kiriko as their second most played, would also acccount for 1 entry. 

Weihgting the values will transform that into Juno=1 and Kiriko=0.5 (sample value, see `actions.ts` for real weight)

Both the raw and weighted values are available in the frontend.

### Gini Coefficient -> Eqality Analysis

(The Gini Coefficient)[https://en.wikipedia.org/wiki/Gini_coefficient] is a measure of inequality.

In short, this value allows you to determine how evenly a distribution of values is spread. In this case, it represents how equally the heroes are played. 

A value of 0 means that the distribution is perfectly even, for example, each hero is picked the same number of times, while a value of 1 indicated there is a very large spread.

In top 500, the occurrence of lower picked heroes is disproportionately low as they simply do not appear in the top 3 very often. For this reason, when calculating the Gini Coefficient, the 10th percentile is excluded from the calculation.


## Issues

The top 500 leaderboards presents some challenges in terms of data collection and validity.

- The top 500 leaderboards get pruned of banned players once the season ends. This means the data must be collected hours before the season ends to get a full 4500 sample.
- Due to a bug with connected accounts, some players appear twice in the leaderboards. This is not accounted for in this project as it impacts approximately 1% of cases, and would skew the data either way.


## License
[WTFPL](/LICENSE)


[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fthearyadev%2Ftop500-aggregator.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fthearyadev%2Ftop500-aggregator?ref=badge_large)
