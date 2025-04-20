import fs from "fs";
import { HeroColors } from "../components/charts/heroColors";

export enum Role {
    DAMAGE = "DAMAGE",
    SUPPORT = "SUPPORT",
    TANK = "TANK",
}

export enum Region {
    AMERICAS = "AMERICAS",
    EUROPE = "EUROPE",
    ASIA = "ASIA",
}

export enum Slot {
    firstMostPlayed = "firstMostPlayed",
    secondMostPlayed = "secondMostPlayed",
    thirdMostPlayed = "thirdMostPlayed",
}

export interface BarChartData {
    labels: string[];
    values: number[];
}

export interface TrendLine {
    name: string;
    data: number[];
}

type RawSeasonDataFile = {
    metadata: { id: number; disclaimer: string };
    entries: {
        role: string;
        region: string;
        firstMostPlayed: string;
        secondMostPlayed: string;
        thirdMostPlayed: string;
    }[];
};

interface Cache {
    [key: number]: RawSeasonDataFile;
}

interface GenericKeyValue {
    [key: string]: number;
}

type WeightedPair = [string, number];

export function calculateStandardDeviation(numbers: number[]): number {
    const sortedNumbers = numbers.slice().sort((a, b) => a - b);
    const percentileIndex = Math.floor(sortedNumbers.length * 0.1);
    const numbersExcludingPercentile = sortedNumbers.slice(percentileIndex);
    const mean =
        numbersExcludingPercentile.reduce((sum, num) => sum + num, 0) /
        numbersExcludingPercentile.length;
    const squaredDifferences = numbersExcludingPercentile.map((num) =>
        Math.pow(num - mean, 2),
    );
    const meanOfSquaredDifferences =
        squaredDifferences.reduce((sum, squaredDiff) => sum + squaredDiff, 0) /
        numbersExcludingPercentile.length;
    const standardDeviation = Math.sqrt(meanOfSquaredDifferences);
    return standardDeviation;
}

export function calculateGiniCoefficient(numbers: number[]): number {
    // removing percentile slice for now.
    // const x_us = numbers.sort((a, b) => a - b);
    // const n = x_us.length;

    // const percentileIndex = Math.floor(n * 0.1);
    // const x = x_us.slice(percentileIndex);

    const x = numbers.sort((a, b) => a - b);
    const n = x.length;

    if (n === 0) return 0;

    let csum: number[] = [];
    for (let i = 0; i < n; i++) {
        csum.push(x.slice(0, i + 1).reduce((a, b) => a + b));
    }
    const total = csum[n - 1];

    const mean = total / n;
    let gini = (n + 1) / n;
    const a = 2 / (n * n * mean);
    const b = x.map((_, i) => (
        (n - i) * x[i]
    )).reduce((a, b) => a + b);

    gini -= a * b;
    return gini;
}

function data_loader_memo(): (seasonNumber: number) => RawSeasonDataFile {
    const cache: Cache = {};
    return function(seasonNumber: number) {
        if (seasonNumber in cache) {
            return cache[seasonNumber];
        }
        const fileContents = fs.readFileSync(
            `../data/season_${seasonNumber}.json`,
        );
        const parsedData: RawSeasonDataFile = JSON.parse(
            fileContents.toString(),
        );
        cache[seasonNumber] = parsedData;
        return cache[seasonNumber];
    };
}

export async function get_season_list(): Promise<number[]> {
    const season_list = fs
        .readdirSync("../data")
        .filter((f) => !f.startsWith("_"))
        .map((f) => Number(f.replace(".json", "").replace("season_", "")))
        .sort((a, b) => a - b);
    return season_list;
}

const load = data_loader_memo();

export function map_generic_kv_to_bar_chart_data(
    data: GenericKeyValue,
): BarChartData {
    const items = Object.entries(data);
    items.sort((a, b) => b[1] - a[1]);
    const labels = items.map((item) => item[0]);
    const values = items.map((item) => item[1]);

    return {
        labels: labels,
        values: values,
    };
}

export async function get_disclaimer(seasonNumber: number): Promise<string> {
    return load(seasonNumber).metadata.disclaimer;
}
enum Weights {
    firstMostPlayed = 1,
    secondMostPlayed = 0.6268,
    thirdMostPlayed = 0.4555,
}

export async function get_occurrences(
    role: Role | null,
    region: Region | null,
    slot: Slot | null,
    seasonNumber: number,
    weighted: boolean = false,
): Promise<GenericKeyValue> {
    let data = load(seasonNumber).entries;
    let slotted_unpacked: WeightedPair[];
    if (role) {
        data = data.filter((e) => e.role === role.toString());
    }

    if (region) {
        data = data.filter((e) => e.region === region.toString());
    }

    if (slot) {
        slotted_unpacked = data.map((e) => [e[slot], Weights.firstMostPlayed]);
    } else {
        slotted_unpacked = data.flatMap(
            ({ firstMostPlayed, secondMostPlayed, thirdMostPlayed }) => [
                [firstMostPlayed, (weighted ? Weights.firstMostPlayed: 1)],
                [secondMostPlayed, (weighted ? Weights.secondMostPlayed: 1)],
                [thirdMostPlayed, (weighted ? Weights.thirdMostPlayed: 1)]
            ],
        );
    }

    return slotted_unpacked
        .filter((pair) => pair[0] !== "Blank")
        .reduce((accumulator, pair) => {
            if (pair[0] in accumulator) {
                accumulator[pair[0]] += pair[1];
            } else {
                accumulator[pair[0]] = pair[1];
            }
            return accumulator;
        }, {} as GenericKeyValue);
}

interface IntermediateDataRep {
    [key: string]: number[];
}

function map_intermediate_data_rep_to_trend_lines(
    lines: IntermediateDataRep,
): TrendLine[] {
    return Object.entries(lines).map(([hero, points]) => ({
        name: hero,
        data: points,
    }));
}

export async function get_occurrence_trend_lines(weighted: boolean = false): Promise<TrendLine[]> {
    const seasonsData = await Promise.all(
        (await get_season_list()).map(
            async (season) => await get_occurrences(null, null, null, season, weighted),
        ),
    );
    const lines: IntermediateDataRep = {};
    for (const seasonData of seasonsData) {
        for (const [hero, count] of Object.entries(seasonData)) {
            lines[hero] = lines[hero] ? [...lines[hero], count] : [count];
        }
        // ensure that all heroes exist
        for (const hero of Object.keys(HeroColors)) {
            if (!(hero in lines)) {
                lines[hero] = [0];
            }
        }
        // ensure that all lines have the same length, if not, append a zero
        const longestLength = Math.max(
            ...Object.values(lines).map((arr) => arr.length),
        );
        for (const [_, points] of Object.entries(lines)) {
            if (points.length != longestLength) {
                points.push(0);
            }
        }
    }
    return map_intermediate_data_rep_to_trend_lines(lines);
}

export async function get_gini_coefficient_trend_lines(): Promise<TrendLine[]> {
    const lines: IntermediateDataRep = {};
    const roles = [Role.SUPPORT, Role.TANK, Role.DAMAGE];
    const season_list = await get_season_list();

    for (const role of roles) {
        for (const season of season_list) {
            const data = await get_occurrences(role, null, Slot.firstMostPlayed, season);
            lines[role] = lines[role] || [];
            lines[role].push(calculateGiniCoefficient(Object.values(data)));
        }
    }
    return map_intermediate_data_rep_to_trend_lines(lines);
}
