import React from "react";
import { Card } from "@/app/components";
import { BarChart } from "@/app/components";
import TopMatter from "@/app/components/topmatter/topmatter";
import {
    Region,
    Role,
    Slot,
    calculateGiniCoefficient,
    calculateStandardDeviation,
    get_disclaimer,
    get_occurrences,
    get_season_list,
    map_generic_kv_to_bar_chart_data,
} from "@/app/server/actions";

export async function generateStaticParams() {
    return (await get_season_list()).map((season) => ({
        seasonNumber: season.toString(),
    }));
}

const HeroStdDev = ({ value, role }: { value: number; role: string }) => {
    return (
        <div className="text-center pt-5 pb-5">
            <h5>{role}</h5>
            <h6 className="text-lg text-center">
                {Math.round((value + Number.EPSILON) * 100) / 100}
            </h6>
        </div>
    );
};

const SeasonPage = async ({ params }: { params: { seasonNumber: number } }) => {
    const regions = [Region.AMERICAS, Region.EUROPE, Region.ASIA];
    const roles = [Role.SUPPORT, Role.DAMAGE, Role.TANK];
    return (
        <main>
            <TopMatter
                seasonNumber={params.seasonNumber.toString()}
                disclaimer={await get_disclaimer(params.seasonNumber)}
            />
            <Card
                title="Role Gini Coeffficient: First Most Played, All Regions"
                subtitle="The Gini Coefficient is a measure of inequality. A higher value indicates greater inequality. A value approaching 0 indicated perfect quality. For example, [1, 1, 1, 1] = 0. This calculation is made with the 10th percentile excluded. The nature of top 500 means that the lesser picked heroes are disproportionately picked, and therefore heavily skew the data."
            >
                <HeroStdDev
                    role="SUPPORT"
                    value={calculateGiniCoefficient(
                        Object.values(
                            await get_occurrences(
                                Role.SUPPORT,
                                null,
                                Slot.firstMostPlayed,
                                params.seasonNumber,
                            ),
                        ),
                    )}
                />
                <HeroStdDev
                    role="DAMAGE"
                    value={calculateGiniCoefficient(
                        Object.values(
                            await get_occurrences(
                                Role.DAMAGE,
                                null,
                                Slot.firstMostPlayed,
                                params.seasonNumber,
                            ),
                        ),
                    )}
                />
                <HeroStdDev
                    role="TANK"
                    value={calculateGiniCoefficient(
                        Object.values(
                            await get_occurrences(
                                Role.TANK,
                                null,
                                Slot.firstMostPlayed,
                                params.seasonNumber,
                            ),
                        ),
                    )}
                />
            </Card>
            <Card title="Hero Occurrences: All Slots" nowrap>
                <BarChart
                    title="Americas"
                    graph={map_generic_kv_to_bar_chart_data(
                        await get_occurrences(
                            null,
                            Region.AMERICAS,
                            null,
                            params.seasonNumber,
                        ),
                    )}
                    maxY={500}
                />
                <BarChart
                    title="Europe"
                    graph={map_generic_kv_to_bar_chart_data(
                        await get_occurrences(
                            null,
                            Region.EUROPE,
                            null,
                            params.seasonNumber,
                        ),
                    )}
                    maxY={500}
                />
                <BarChart
                    title="Asia"
                    graph={map_generic_kv_to_bar_chart_data(
                        await get_occurrences(
                            null,
                            Region.ASIA,
                            null,
                            params.seasonNumber,
                        ),
                    )}
                    maxY={500}
                />
                <BarChart
                    title="All Regions"
                    graph={map_generic_kv_to_bar_chart_data(
                        await get_occurrences(
                            null,
                            null,
                            null,
                            params.seasonNumber,
                        ),
                    )}
                    maxY={1200}
                />
            </Card>
            <Card title="Hero Occurrences: First Most Played">
                {roles.map((role) => {
                    return regions.map(async (region) => {
                        return (
                            <BarChart
                                title={`${role}: ${region}`}
                                graph={map_generic_kv_to_bar_chart_data(
                                    await get_occurrences(
                                        role,
                                        region,
                                        Slot.firstMostPlayed,
                                        params.seasonNumber,
                                    ),
                                )}
                                maxY={300}
                            />
                        );
                    });
                })}
                {roles.map(async (role) => {
                    return (
                        <BarChart
                            title={`${role}: All`}
                            graph={map_generic_kv_to_bar_chart_data(
                                await get_occurrences(
                                    role,
                                    null,
                                    Slot.firstMostPlayed,
                                    params.seasonNumber,
                                ),
                            )}
                            maxY={500}
                        />
                    );
                })}
            </Card>
            <Card title="Hero Occurrences: Second Most Played">
                {roles.map((role) => {
                    return regions.map(async (region) => {
                        return (
                            <BarChart
                                title={`${role}: ${region}`}
                                graph={map_generic_kv_to_bar_chart_data(
                                    await get_occurrences(
                                        role,
                                        region,
                                        Slot.secondMostPlayed,
                                        params.seasonNumber,
                                    ),
                                )}
                                maxY={300}
                            />
                        );
                    });
                })}
                {roles.map(async (role) => {
                    return (
                        <BarChart
                            title={`${role}: All`}
                            graph={map_generic_kv_to_bar_chart_data(
                                await get_occurrences(
                                    role,
                                    null,
                                    Slot.secondMostPlayed,
                                    params.seasonNumber,
                                ),
                            )}
                            maxY={500}
                        />
                    );
                })}
            </Card>
            <Card title="Hero Occurrences: Third Most Played">
                {roles.map((role) => {
                    return regions.map(async (region) => {
                        return (
                            <BarChart
                                title={`${role}: ${region}`}
                                graph={map_generic_kv_to_bar_chart_data(
                                    await get_occurrences(
                                        role,
                                        region,
                                        Slot.thirdMostPlayed,
                                        params.seasonNumber,
                                    ),
                                )}
                                maxY={300}
                            />
                        );
                    });
                })}
                {roles.map(async (role) => {
                    return (
                        <BarChart
                            title={`${role}: All`}
                            graph={map_generic_kv_to_bar_chart_data(
                                await get_occurrences(
                                    role,
                                    null,
                                    Slot.thirdMostPlayed,
                                    params.seasonNumber,
                                ),
                            )}
                            maxY={500}
                        />
                    );
                })}
            </Card>
        </main>
    );
};

export default SeasonPage;
