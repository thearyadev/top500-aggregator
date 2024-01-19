"use server";

const backendUrl = process.env.BACKEND_URL;
export type Statistic = {
    mean: number;
    standard_deviation: number;
    variance: number;
}

export type BarChartData = {
    labels: string[];
    values: number[];
}

export type SingleChart = {
    graph: BarChartData;
    statistic: Statistic;
}

export type SeasonData = {
    [key: string]: SingleChart
}

export type StdDevs = {
    DAMAGE: number;
    SUPPORT: number;
    TANK: number;
}

export type TrendLine = {
    name: string;
    data: number[]
}

export async function fetchSingleSeasonPageChartData(seasonNumber: number): Promise<SingleChart[]> {
    const response = await fetch(`${backendUrl}/chart/${seasonNumber}_8`);
    return await response.json();
}


export async function fetchSeasonList(): Promise<string[]> {
    const response = await fetch(`${backendUrl}/d/seasons`)
    return await response.json()
}


export async function fetchSingleSeasonStdDevs(seasonNumber: number): Promise<StdDevs> {
    const response = await fetch(`${backendUrl}/d/single_season_std_by_role/${seasonNumber}_8`)
    return await response.json()
}

export async function fetchSeasonalOccurrenceTrend(): Promise<TrendLine[]>{
    const response = await fetch(`${backendUrl}/chart/trend/d`)
    return await response.json()
}

export async function fetchSeasonalStdDevTrendByRole(): Promise<TrendLine[]>{
    const response = await fetch(`${backendUrl}/d/all_seasons_std_by_role`)
    return await response.json()
}
